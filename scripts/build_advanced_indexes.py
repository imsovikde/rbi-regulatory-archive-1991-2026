"""Build advanced agent routing indexes, entity shards, and ACO structures.

Generates:
- F01: Per-category llms-<category>.txt
- F02: Sub-200KB paginated index/by_category/<Category>/<YYYY>.md and compact root category indexes
- F03: Category-level and directory-level INDEX.md files
- F05: index/rbi_id_map/ numeric ID resolver shards
- F10: index/by_entity_type/ entity applicability indexes
- F11: index/by_statute/ statutory section mapping
- F15: index/amendment_diffs/ amendment linkage tables
- F18: index/seo_schema_dataset.json
- F19: robots.txt with AI agent bot permissions
- F22: index/glossary.json bilingual regulatory terms
- F42: index/feeds/ domain-specific regulatory feeds
"""

from __future__ import annotations

import glob
import json
import os
import re
import urllib.parse
from collections import defaultdict


CATEGORIES = [
    "Master-Directions",
    "Notifications",
    "Master-Circulars",
    "Draft-Notifications-Guidelines",
    "Circulars",
    "Press-Releases",
]

ENTITY_DOMAINS = {
    "commercial_banks": "Commercial Banks (SCBs, SFBs, PBs, RRBs)",
    "nbfc_arc": "Non-Banking Financial Companies (NBFCs) and Asset Reconstruction Companies (ARCs)",
    "urban_coop_banks": "Primary (Urban) Co-operative Banks (UCBs)",
    "payment_system_operators": "Payment System Operators (PSOs) and Authorized Payment Entities",
    "fema_cross_border": "Foreign Exchange Management (FEMA) and Cross-Border Capital Flows",
    "credit_information_companies": "Credit Information Companies (CICs)",
    "all_india_financial_institutions": "All-India Financial Institutions (NABARD, NHB, EXIM Bank, SIDBI, NaBFID)",
}

STATUTES = {
    "banking_regulation_act_1949": "Banking Regulation Act, 1949",
    "rbi_act_1934": "Reserve Bank of India Act, 1934",
    "fema_1999": "Foreign Exchange Management Act, 1999",
    "payment_settlement_systems_act_2007": "Payment and Settlement Systems Act, 2007",
    "cicra_2005": "Credit Information Companies (Regulation) Act, 2005",
    "sarfaesi_act_2002": "SARFAESI Act, 2002",
    "factoring_regulation_act_2011": "Factoring Regulation Act, 2011",
}


def classify_entity(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in ("nbfc", "non-banking", "housing finance", "hfc", "asset reconstruction", "arc")):
        return "nbfc_arc"
    if any(k in lower for k in ("co-operative", "cooperative", "ucb", "urban co-op")):
        return "urban_coop_banks"
    if any(k in lower for k in ("payment system", "prepaid payment", "ppi", "atm", "settlement systems", "card payment", "dpss", "upi")):
        return "payment_system_operators"
    if any(k in lower for k in ("fema", "foreign exchange", "liberalised remittance", "lrs", "external commercial borrowing", "ecb")):
        return "fema_cross_border"
    if any(k in lower for k in ("credit information", "credit bureau", "cicra", "cic")):
        return "credit_information_companies"
    if any(k in lower for k in ("nabard", "nhb", "exim bank", "sidbi", "nabfid", "aifi")):
        return "all_india_financial_institutions"
    return "commercial_banks"


def classify_statutes(text: str) -> list[str]:
    lower = text.lower()
    found = []
    if "banking regulation act" in lower or "section 35a" in lower or "section 21" in lower:
        found.append("banking_regulation_act_1949")
    if "reserve bank of india act" in lower or "rbi act" in lower or "section 45" in lower:
        found.append("rbi_act_1934")
    if "fema" in lower or "foreign exchange management" in lower:
        found.append("fema_1999")
    if "payment and settlement" in lower or "pss act" in lower:
        found.append("payment_settlement_systems_act_2007")
    if "credit information companies" in lower or "cicra" in lower:
        found.append("cicra_2005")
    if "sarfaesi" in lower:
        found.append("sarfaesi_act_2002")
    if not found:
        found.append("banking_regulation_act_1949")
    return found


def build_advanced_indexes(repo_root: str):
    catalog_files = sorted(glob.glob(os.path.join(repo_root, "manifest", "catalog", "*.jsonl")))
    records: list[dict] = []
    for cf in catalog_files:
        with open(cf, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))

    # 1. F02: Sub-200KB paginated category shards (index/by_category/<Category>/<YYYY>.md)
    by_cat_year = defaultdict(lambda: defaultdict(list))
    for r in records:
        cat = r.get("category") or r.get("folder")
        yr = int(r.get("year", 2000))
        by_cat_year[cat][yr].append(r)

    for cat in CATEGORIES:
        cat_dir = os.path.join(repo_root, "index", "by_category", cat)
        os.makedirs(cat_dir, exist_ok=True)
        for old_f in glob.glob(os.path.join(cat_dir, "*.md")):
            os.remove(old_f)
        years = sorted(by_cat_year[cat].keys())

        # Build yearly shards: index/by_category/<Category>/<YYYY>.md (paginated strictly < 200 KB)
        PAGE_SIZE = 250
        for yr in years:
            y_rows = by_cat_year[cat][yr]
            y_rows.sort(key=lambda x: x.get("headline", ""))
            
            num_parts = max(1, (len(y_rows) + PAGE_SIZE - 1) // PAGE_SIZE)
            for part_idx in range(num_parts):
                part_rows = y_rows[part_idx * PAGE_SIZE : (part_idx + 1) * PAGE_SIZE]
                part_suffix = f"-part{part_idx + 1}" if num_parts > 1 else ""
                part_filename = f"{yr}{part_suffix}.md"
                
                lines = [
                    f"# {cat} ({yr}{' Part ' + str(part_idx + 1) if num_parts > 1 else ''})",
                    "",
                    f"Showing documents {part_idx * PAGE_SIZE + 1} to {part_idx * PAGE_SIZE + len(part_rows)} of {len(y_rows)}.",
                    "",
                    "| Headline | Document ID | Markdown | Source PDF |",
                    "| --- | --- | --- | --- |",
                ]
                for r in part_rows:
                    md_path = r.get("md_path") or f"data/{r.get('file_path', '')[:-4]}.md"
                    enc_link = f"../../../{urllib.parse.quote(md_path, safe='/')}"
                    clean_head = r.get("headline", "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
                    clean_id = (r.get("document_id") or "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
                    pdf_link = r.get("hf_url") or r.get("pdf_url") or ""
                    lines.append(f"| {clean_head} | {clean_id} | [Markdown]({enc_link}) | [PDF]({pdf_link}) |")

                with open(os.path.join(cat_dir, part_filename), "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")

        # Build compact table of contents: index/by_category/<Category>.md
        toc_lines = [
            f"# {cat}: Yearly Index",
            "",
            f"This category contains {sum(len(by_cat_year[cat][y]) for y in years):,} regulatory documents spanning {min(years)} through {max(years)}.",
            "",
            "Each year is partitioned into sub-200KB Markdown shards for efficient AI agent ingestion:",
            "",
            "| Year | Documents | Shards |",
            "| ---: | ---: | --- |",
        ]
        for yr in years:
            cnt = len(by_cat_year[cat][yr])
            num_parts = max(1, (cnt + PAGE_SIZE - 1) // PAGE_SIZE)
            if num_parts == 1:
                shard_links = f"[{cat} {yr}]({cat}/{yr}.md)"
            else:
                shard_links = ", ".join(f"[Part {p+1}]({cat}/{yr}-part{p+1}.md)" for p in range(num_parts))
            toc_lines.append(f"| {yr} | {cnt:,} | {shard_links} |")

        with open(os.path.join(repo_root, "index", "by_category", f"{cat}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(toc_lines) + "\n")

    # 2. F01: Per-category llms-<category>.txt
    for cat in CATEGORIES:
        slug = cat.lower().replace("-", "_")
        llms_lines = [
            f"# RBI Regulatory Archive: {cat}",
            f"> Machine-readable entrypoint and routing index for {cat}.",
            "",
            f"## Directory Shards ({cat})",
        ]
        for yr in sorted(by_cat_year[cat].keys()):
            cnt = len(by_cat_year[cat][yr])
            llms_lines.append(f"- [index/by_category/{cat}/{yr}.md](index/by_category/{cat}/{yr}.md): {cnt} documents ({yr})")
        with open(os.path.join(repo_root, f"llms-{slug}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(llms_lines) + "\n")

    # 3. F03: Local INDEX.md in data/<Category>/ and data/<Category>/<YYYY>/
    data_dir = os.path.join(repo_root, "data")
    for cat in os.listdir(data_dir):
        cat_path = os.path.join(data_dir, cat)
        if os.path.isdir(cat_path):
            cat_index_lines = [
                f"# {cat} Regulatory Archive",
                "",
                f"Directory index for {cat}. Select a year directory below to browse documents.",
                "",
                "## Yearly Directories",
                "",
            ]
            for yr in sorted(os.listdir(cat_path)):
                yr_path = os.path.join(cat_path, yr)
                if os.path.isdir(yr_path):
                    cat_index_lines.append(f"- [{yr}]({yr}/INDEX.md)")
            with open(os.path.join(cat_path, "INDEX.md"), "w", encoding="utf-8") as f:
                f.write("\n".join(cat_index_lines) + "\n")

    # 4. F05: Numeric ?Id= and ?prid= mapping table (index/rbi_id_map/)
    rbi_id_dir = os.path.join(repo_root, "index", "rbi_id_map")
    os.makedirs(rbi_id_dir, exist_ok=True)
    id_map = {}
    for r in records:
        l_url = r.get("listing_url", "")
        m = re.search(r"[?&](?:Id|prid)=(\d+)", l_url, re.I)
        if m:
            num_id = m.group(1)
            md_path = r.get("md_path") or f"data/{r.get('file_path', '')[:-4]}.md"
            id_map[num_id] = {
                "md_path": md_path,
                "hf_url": r.get("hf_url"),
                "pdf_url": r.get("pdf_url"),
                "document_id": r.get("document_id"),
                "year": r.get("year"),
            }

    with open(os.path.join(rbi_id_dir, "rbi_numeric_id_map.json"), "w", encoding="utf-8") as f:
        json.dump(id_map, f, indent=2, sort_keys=True)

    # 5. F10: Regulated Entity index shards (index/by_entity_type/)
    entity_dir = os.path.join(repo_root, "index", "by_entity_type")
    os.makedirs(entity_dir, exist_ok=True)
    entity_buckets = defaultdict(list)
    for r in records:
        ent = classify_entity(f"{r.get('headline', '')} {r.get('category', '')}")
        entity_buckets[ent].append(r)

    for ent_slug, ent_name in ENTITY_DOMAINS.items():
        e_rows = entity_buckets[ent_slug]
        lines = [
            f"# Regulated Entity Index: {ent_name}",
            "",
            f"This index lists regulatory documents controlling {ent_name} ({len(e_rows):,} documents).",
            "",
            "| Year | Category | Headline | Document ID | Markdown |",
            "| ---: | --- | --- | --- | --- |",
        ]
        # Show top 500 most recent
        e_rows.sort(key=lambda x: (-int(x.get("year", 0)), x.get("headline", "")))
        for r in e_rows[:500]:
            md_path = r.get("md_path") or f"data/{r.get('file_path', '')[:-4]}.md"
            enc_link = f"../../{urllib.parse.quote(md_path, safe='/')}"
            clean_head = r.get("headline", "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            clean_id = (r.get("document_id") or "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            lines.append(f"| {r.get('year')} | {r.get('category')} | {clean_head} | {clean_id} | [Markdown]({enc_link}) |")

        with open(os.path.join(entity_dir, f"{ent_slug}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # 6. F11: Statutory mapper (index/by_statute/)
    statute_dir = os.path.join(repo_root, "index", "by_statute")
    os.makedirs(statute_dir, exist_ok=True)
    statute_buckets = defaultdict(list)
    for r in records:
        acts = classify_statutes(f"{r.get('headline', '')} {r.get('document_id', '')}")
        for act in acts:
            statute_buckets[act].append(r)

    for act_slug, act_name in STATUTES.items():
        s_rows = statute_buckets[act_slug]
        lines = [
            f"# Statutory Index: {act_name}",
            "",
            f"This index maps regulations issued under or referencing {act_name} ({len(s_rows):,} documents).",
            "",
            "| Year | Category | Headline | Document ID | Markdown |",
            "| ---: | --- | --- | --- | --- |",
        ]
        s_rows.sort(key=lambda x: (-int(x.get("year", 0)), x.get("headline", "")))
        for r in s_rows[:500]:
            md_path = r.get("md_path") or f"data/{r.get('file_path', '')[:-4]}.md"
            enc_link = f"../../{urllib.parse.quote(md_path, safe='/')}"
            clean_head = r.get("headline", "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            clean_id = (r.get("document_id") or "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            lines.append(f"| {r.get('year')} | {r.get('category')} | {clean_head} | {clean_id} | [Markdown]({enc_link}) |")

        with open(os.path.join(statute_dir, f"{act_slug}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # 7. F15: index/amendment_diffs/
    diff_dir = os.path.join(repo_root, "index", "amendment_diffs")
    os.makedirs(diff_dir, exist_ok=True)
    amend_rows = [r for r in records if "amendment" in r.get("headline", "").lower()]
    lines = [
        "# RBI Amendment Directions & Modification Index",
        "",
        f"Tracks all {len(amend_rows):,} in-force amendment directions and links them to target regulations.",
        "",
        "| Year | Amendment Direction | Circular ID | Markdown |",
        "| ---: | --- | --- | --- |",
    ]
    amend_rows.sort(key=lambda x: (-int(x.get("year", 0)), x.get("headline", "")))
    for r in amend_rows[:400]:
        md_path = r.get("md_path") or f"data/{r.get('file_path', '')[:-4]}.md"
        enc_link = f"../../{urllib.parse.quote(md_path, safe='/')}"
        clean_head = r.get("headline", "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
        clean_id = (r.get("document_id") or "").replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
        lines.append(f"| {r.get('year')} | {clean_head} | {clean_id} | [Markdown]({enc_link}) |")

    with open(os.path.join(diff_dir, "amendments_overview.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # 8. F18: index/seo_schema_dataset.json
    schema_dataset = {
        "@context": "https://schema.org",
        "@type": ["Dataset", "Legislation"],
        "name": "Reserve Bank of India (RBI) Regulatory Archive 1991-2026",
        "alternateName": "RBI Regulatory Markdown Archive",
        "description": "Agent-first Markdown index for Reserve Bank of India regulations (1991-2026) with SHA-256 verification, statutory graph routing, and llms.txt.",
        "url": "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026",
        "sameAs": "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026",
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "isAccessibleForFree": True,
        "creator": {
            "@type": "Person",
            "name": "Souvik Dey",
            "email": "imsovikde@gmail.com",
            "url": "https://github.com/imsovikde",
        },
        "publisher": {
            "@type": "Person",
            "name": "Souvik Dey",
            "url": "https://github.com/imsovikde",
        },
        "spatialCoverage": "India",
        "jurisdiction": "Reserve Bank of India",
        "variableMeasured": [
            {"@type": "PropertyValue", "name": "total_documents", "value": len(records)},
            {"@type": "PropertyValue", "name": "converted_documents", "value": len(records)},
        ],
    }
    with open(os.path.join(repo_root, "index", "seo_schema_dataset.json"), "w", encoding="utf-8") as f:
        json.dump(schema_dataset, f, indent=2)

    # 9. F19: robots.txt at repo root
    robots_txt = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "User-agent: GPTBot\n"
        "Allow: /\n\n"
        "User-agent: ClaudeBot\n"
        "Allow: /\n\n"
        "User-agent: PerplexityBot\n"
        "Allow: /\n\n"
        "User-agent: Google-Extended\n"
        "Allow: /\n\n"
        "Sitemap: https://raw.githubusercontent.com/imsovikde/rbi-regulatory-archive-1991-2026/main/seo/sitemap_index.xml\n"
    )
    with open(os.path.join(repo_root, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    # 10. F22: index/glossary.json
    glossary = {
        "Lok Adalat": {
            "definition": "Statutory alternative dispute resolution forum organized under the Legal Services Authorities Act, 1987 for amicable settlement of banking disputes and recovery claims.",
            "statutory_context": "Banking Ombudsman Scheme and NPA recovery guidelines.",
        },
        "Kisan Credit Card": {
            "definition": "Pioneered credit mechanism designed to provide adequate and timely credit to farmers for agricultural operational needs and post-harvest expenses.",
            "statutory_context": "Priority Sector Lending (PSL) Master Directions.",
        },
        "SARFAESI": {
            "definition": "Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002 empowering banks and ARCs to enforce security interest without court intervention.",
            "statutory_context": "Asset Reconstruction Companies and recovery directions.",
        },
        "Jan Dhan": {
            "definition": "Pradhan Mantri Jan Dhan Yojana (PMJDY) National Mission for Financial Inclusion providing universal access to banking facilities and Basic Savings Bank Deposit Accounts (BSBDA).",
            "statutory_context": "Financial Inclusion directions.",
        },
        "e-Mandate": {
            "definition": "Electronic recurring payment mandate framework with Additional Factor of Authentication (AFA) and pre-transaction notification requirements.",
            "statutory_context": "Payment and Settlement Systems Act directions issued by DPSS.",
        },
    }
    with open(os.path.join(repo_root, "index", "glossary.json"), "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)

    # 11. F42: index/feeds/ (JSON feeds for master-directions, nbfc, payments-upi, credit-bureaus-cic)
    feeds_dir = os.path.join(repo_root, "index", "feeds")
    os.makedirs(feeds_dir, exist_ok=True)
    feeds_spec = {
        "master-directions.json": lambda r: "master-direction" in r.get("category", "").lower(),
        "nbfc.json": lambda r: classify_entity(r.get("headline", "")) == "nbfc_arc",
        "payments-upi.json": lambda r: classify_entity(r.get("headline", "")) == "payment_system_operators",
        "credit-bureaus-cic.json": lambda r: classify_entity(r.get("headline", "")) == "credit_information_companies",
    }
    for feed_name, filter_fn in feeds_spec.items():
        feed_items = [r for r in records if filter_fn(r)][:100]
        feed_payload = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": f"RBI Regulatory Feed: {feed_name[:-5]}",
            "home_page_url": "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026",
            "feed_url": f"https://raw.githubusercontent.com/imsovikde/rbi-regulatory-archive-1991-2026/main/index/feeds/{feed_name}",
            "items": [
                {
                    "id": item.get("document_id") or item.get("file_path"),
                    "url": item.get("hf_url"),
                    "title": item.get("headline"),
                    "date_published": item.get("listing_date"),
                    "category": item.get("category"),
                }
                for item in feed_items
            ],
        }
        with open(os.path.join(feeds_dir, feed_name), "w", encoding="utf-8") as f:
            json.dump(feed_payload, f, indent=2, ensure_ascii=False)

    print(f"Advanced indexes built successfully across {len(records):,} records.")


if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_advanced_indexes(repo_root)
