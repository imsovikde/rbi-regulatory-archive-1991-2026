"""Statutory indexer and agent routing engine for the RBI Regulatory Archive.

Builds deterministic agent-first routing layers under index/agent_router/:
- TRIAGE_GUIDE.md: 5-tier regulatory hierarchy & <= 3 tool call retrieval protocol.
- active_master_directions_by_entity.md & .json: Master Directions mapped by entity.
- circular_ref_to_path.json: Official circular reference numbers to .md file paths.
- citation_and_consequence_graph.jsonl: Causal law graph (AMENDS, REPEALS, CITES, PENALIZES_UNDER).
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from urllib.parse import quote

__all__ = ["build_agent_router", "md_path_for"]


def md_path_for(file_path: str) -> str:
    stem = file_path[:-4] if file_path.lower().endswith(".pdf") else file_path
    return "data/" + stem + ".md"


def _safe_read_frontmatter(full_path: str) -> dict:
    if os.name == "nt" and not full_path.startswith("\\\\?\\"):
        full_path = "\\\\?\\" + os.path.abspath(full_path)
    if not os.path.exists(full_path):
        return {}
    fm = {}
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            line = f.readline()
            if not line.startswith("---"):
                return {}
            for line in f:
                if line.startswith("---"):
                    break
                if ":" in line:
                    k, _, v = line.partition(":")
                    fm[k.strip()] = v.strip().strip('"')
    except Exception:
        pass
    return fm


def _classify_master_direction_entity(title: str, headline: str) -> str:
    text = f"{title} {headline}".lower()
    if any(k in text for k in ("nbfc", "non-banking", "scale based regulation", "core investment", "housing finance", "hfc", "asset reconstruction", "arc")):
        if "housing finance" in text or "hfc" in text:
            return "Housing Finance Companies (HFCs)"
        return "Non-Banking Financial Companies (NBFCs & ARCs)"
    if any(k in text for k in ("co-operative", "cooperative", "ucb", "urban co-op", "stcb", "dccb")):
        return "Primary (Urban) Co-operative Banks (UCBs)"
    if any(k in text for k in ("payment system", "prepaid payment", "ppi", "atm", "settlement systems", "card payment", "cards and payment", "dpss")):
        return "Payment System Operators (PSOs) & Authorized Payment Entities"
    if any(k in text for k in ("fema", "foreign exchange", "liberalised remittance", "lrs", "remittance", "external commercial borrowing", "ecb", "export of goods", "import of goods", "non-resident", "borrowing and lending")):
        return "Foreign Exchange Management (FEMA) & Cross-Border"
    if any(k in text for k in ("financial market", "money market", "derivatives", "interest rate", "repo", "hedging", "g-sec", "government securities", "commercial paper")):
        return "Financial Markets, Money Market & Derivatives"
    if any(k in text for k in ("kyc", "know your customer", "anti-money laundering", "cyber security", "customer service", "outsourcing", "fraud", "conduct")):
        return "Cross-Sectoral, Governance & Consumer Protection"
    if any(k in text for k in ("commercial bank", "banks", "banking", "capital adequacy", "basel", "priority sector", "credit risk", "liquidity risk")):
        return "Commercial Banks (SCBs, SFBs, PBs, RRBs)"
    return "All-India Financial Institutions & Miscellaneous"


def _extract_references(text: str) -> list[str]:
    refs = set()
    for m in re.finditer(r"\b(RBI/\d{4}-\d{2,4}/\d+)\b", text, re.IGNORECASE):
        refs.add(m.group(1).upper())
    for m in re.finditer(r"\b([A-Z]{2,6}\.(?:[A-Za-z0-9\.-]+)/(?:[A-Za-z0-9\.-]+))\b", text):
        refs.add(m.group(1))
    for m in re.finditer(r"\b([A-Z]{2,6}\.No\.[A-Za-z0-9\.-]+)\b", text):
        refs.add(m.group(1))
    return sorted(refs)


def build_agent_router(repo_root: str, inventory_rows: list[dict], ledger_rows: list[dict]) -> dict:
    router_dir = os.path.join(repo_root, "index", "agent_router")
    os.makedirs(router_dir, exist_ok=True)

    ledger_by_path = {r.get("file_path"): r for r in ledger_rows if r.get("file_path")}

    # 1. Circular Ref to Path Mapping
    circular_map = {}
    graph_records = []

    statutory_patterns = [
        (re.compile(r"Section\s+35A", re.I), "Banking Regulation Act, 1949 (Section 35A - Power to issue directions)"),
        (re.compile(r"Section\s+21\b", re.I), "Banking Regulation Act, 1949 (Section 21 - Control over advances)"),
        (re.compile(r"Section\s+45JA", re.I), "Reserve Bank of India Act, 1934 (Section 45JA - Powers over NBFCs)"),
        (re.compile(r"Section\s+45L\b", re.I), "Reserve Bank of India Act, 1934 (Section 45L - Directions to financial institutions)"),
        (re.compile(r"Section\s+45W\b", re.I), "Reserve Bank of India Act, 1934 (Section 45W - Regulation of financial markets)"),
        (re.compile(r"Section\s+47A\b", re.I), "Banking Regulation Act, 1949 (Section 47A - Monetary Penalties)"),
        (re.compile(r"Section\s+58G\b", re.I), "Reserve Bank of India Act, 1934 (Section 58G - Penalties on NBFCs)"),
        (re.compile(r"Section\s+18\b", re.I), "Payment and Settlement Systems Act, 2007 (Section 18 - Power to issue directions)"),
        (re.compile(r"Section\s+10\b", re.I), "Payment and Settlement Systems Act, 2007 (Section 10 - Power to regulate)"),
        (re.compile(r"FEMA\s+1999|Foreign\s+Exchange\s+Management", re.I), "Foreign Exchange Management Act, 1999 (FEMA)"),
    ]

    for row in inventory_rows:
        file_path = row.get("file_path", "")
        md_path = md_path_for(file_path)
        doc_id = (row.get("document_id") or "").strip()
        headline = (row.get("headline") or "").strip()
        year = row.get("year", 0)
        cat = row.get("category", "")

        if doc_id:
            circular_map[doc_id] = md_path
            norm_id = re.sub(r"[\s\.-]+", "", doc_id).upper()
            if norm_id:
                circular_map[norm_id] = md_path

        found_refs = _extract_references(headline)
        for ref in found_refs:
            circular_map[ref] = md_path
            norm_ref = re.sub(r"[\s\.-]+", "", ref).upper()
            if norm_ref:
                circular_map[norm_ref] = md_path

        # Causal graph extraction
        lower_head = headline.lower()
        rel = "CITES"
        if "amendment direction" in lower_head or "amends" in lower_head or "modification" in lower_head:
            rel = "AMENDS"
        elif "supersedes" in lower_head or "repeal" in lower_head or "in supersession of" in lower_head:
            rel = "REPEALS"
        elif "monetary penalty" in lower_head or "penalty on" in lower_head or "penalises" in lower_head or "penalizes" in lower_head or "cancels certificate" in lower_head:
            rel = "PENALIZES_UNDER"

        for pat, act in statutory_patterns:
            if pat.search(headline):
                graph_records.append({
                    "source_file": md_path,
                    "target_ref": act,
                    "relationship": rel,
                    "statutory_act": act,
                    "year": year,
                    "category": cat,
                    "context": headline,
                })

        for ref in found_refs:
            graph_records.append({
                "source_file": md_path,
                "target_ref": ref,
                "relationship": rel,
                "statutory_act": "RBI Circulars/Directions",
                "year": year,
                "category": cat,
                "context": headline,
            })

    # Write circular_ref_to_path.json
    ref_map_path = os.path.join(router_dir, "circular_ref_to_path.json")
    with open(ref_map_path, "w", encoding="utf-8") as f:
        json.dump(circular_map, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

    # Write citation_and_consequence_graph.jsonl
    graph_path = os.path.join(router_dir, "citation_and_consequence_graph.jsonl")
    with open(graph_path, "w", encoding="utf-8") as f:
        for rec in graph_records:
            f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")

    # 2. Process Master Directions by Entity
    md_rows = [r for r in inventory_rows if r.get("category") == "Master-Directions" or r.get("file_path", "").startswith("Master-Directions/")]
    entities_map = defaultdict(list)

    for r in md_rows:
        fp = r.get("file_path", "")
        md_path = md_path_for(fp)
        full_md_path = os.path.join(repo_root, md_path)
        fm = _safe_read_frontmatter(full_md_path)
        title = fm.get("title") or r.get("headline") or os.path.basename(fp)
        headline = r.get("headline", "")
        entity = _classify_master_direction_entity(title, headline)
        item = {
            "title": title,
            "document_id": r.get("document_id") or fm.get("doc_id") or "",
            "year": r.get("year") or fm.get("year") or 0,
            "file_path": fp,
            "md_path": md_path,
            "pdf_url": r.get("pdf_url") or fm.get("source_rbi_url") or "",
            "hf_url": r.get("hf_url") or fm.get("source_hf_url") or "",
            "entity": entity,
        }
        entities_map[entity].append(item)

    for entity in entities_map:
        entities_map[entity].sort(key=lambda x: (x["year"], x["title"]))

    # Write active_master_directions_by_entity.json
    md_json_path = os.path.join(router_dir, "active_master_directions_by_entity.json")
    with open(md_json_path, "w", encoding="utf-8") as f:
        json.dump(entities_map, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

    # Write active_master_directions_by_entity.md
    md_doc_lines = [
        "# Active Master Directions by Regulated Entity",
        "",
        "This index organizes all Master Directions issued by the Reserve Bank of India into primary regulated entity domains. Master Directions represent **Tier 1 Controlling Law** and supersede legacy circulars.",
        "",
        "## Table of Contents",
        "",
    ]
    for entity in sorted(entities_map.keys()):
        anchor = re.sub(r"[^a-z0-9]+", "-", entity.lower()).strip("-")
        md_doc_lines.append(f"- [{entity}](#{anchor}) ({len(entities_map[entity])} directions)")
    md_doc_lines.append("")

    for entity in sorted(entities_map.keys()):
        items = entities_map[entity]
        md_doc_lines.append(f"## {entity}")
        md_doc_lines.append("")
        md_doc_lines.append(f"Total: {len(items)} Master Directions.")
        md_doc_lines.append("")
        md_doc_lines.append("| Year | Master Direction Title | Document ID | Markdown | Source PDF |")
        md_doc_lines.append("| ---: | --- | --- | --- | --- |")
        for it in items:
            stem = it["md_path"]
            encoded_link = f"../../{quote(stem.strip(), safe='/')}"
            title_clean = it["title"].replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            doc_id_clean = it["document_id"].replace("|", "\\|").replace("\u2013", "-").replace("\u2014", "-")
            md_doc_lines.append(f"| {it['year']} | {title_clean} | {doc_id_clean} | [Markdown]({encoded_link}) | [PDF]({it['hf_url']}) |")
        md_doc_lines.append("")

    md_doc_path = os.path.join(router_dir, "active_master_directions_by_entity.md")
    with open(md_doc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_doc_lines) + "\n")

    # 3. Write TRIAGE_GUIDE.md
    triage_lines = [
        "# RBI Regulatory Archive: AI Agent Triage and Statutory Hierarchy Guide",
        "",
        f"Welcome, Agent. This repository contains the complete, authoritative, and lossless archive of all Reserve Bank of India (RBI) regulations from 1991 through 2026 ({len(inventory_rows):,}+ documents) converted to GitHub-Flavored Markdown.",
        "",
        "This guide provides a deterministic, zero-hallucination routing protocol for AI agents, RAG engines, and automated legal verification pipelines to locate controlling RBI regulations in $\\le 3$ tool calls.",
        "",
        "---",
        "",
        "## 1. Statutory Regulatory Hierarchy (5 Tiers)",
        "",
        "The Reserve Bank of India governs the Indian financial ecosystem under a strict statutory hierarchy. When answering legal, compliance, or regulatory queries, agents must prioritize controlling law over operational circulars:",
        "",
        "### Tier 1: Controlling Law & Consolidated Master Directions (Highest Authority)",
        "- **Primary Source:** `data/Master-Directions/`",
        "- **Statutory Authority:**",
        "  - Section 35A & Section 21, Banking Regulation Act, 1949",
        "  - Section 45JA, 45L, 45M, & 45W, Reserve Bank of India Act, 1934",
        "  - Sections 10(4), 11(1), & 11(2), Foreign Exchange Management Act (FEMA), 1999",
        "  - Section 10(2) & Section 18, Payment and Settlement Systems Act, 2007",
        "  - Sections 29A & 30A, National Housing Bank Act, 1987 / RBI Act (for HFCs)",
        "- **Operational Rule for Agents:** Master Directions consolidate all previous circulars and notifications on a regulatory subject. They are updated dynamically by the RBI. Whenever an agent needs the prevailing rule or current standard on any topic (e.g. KYC, Capital Adequacy, Basel III, Priority Sector Lending, Digital Lending, Outsourcing), the agent **MUST** cite the corresponding Master Direction first.",
        "- **Index:** `index/agent_router/active_master_directions_by_entity.md` and `.json`.",
        "",
        "### Tier 2: Operational Directives & In-Year Circulars",
        "- **Primary Sources:** `data/Notifications/` and `data/Circulars/`",
        "- **Role:** Specific operational instructions, immediate policy rate revisions (Repo/Reverse Repo/SDF), regulatory reporting formats, or interim amendments issued between annual consolidations of Master Directions.",
        "- **Operational Rule for Agents:** If an inquiry asks about a specific circular number (e.g., `RBI/2025-26/123`), look it up directly via `index/agent_router/circular_ref_to_path.json`. To verify whether a circular amends or is superseded by a Master Direction, check `index/agent_router/citation_and_consequence_graph.jsonl`.",
        "",
        "### Tier 3: Draft Guidelines & Consultative Documents",
        "- **Primary Source:** `data/Draft-Notifications-Guidelines/`",
        "- **Role:** Proposed regulatory frameworks released for public comments and stakeholder feedback (e.g. Draft Framework on Climate Risk, Draft Directions on Project Finance).",
        "- **Operational Rule for Agents:** **NON-BINDING.** Agents must never present draft guidelines as enforceable law. Always qualify citations with *\"Draft / For feedback only.\"*",
        "",
        "### Tier 4: Penal Consequences & Enforcement Actions",
        "- **Primary Source:** `data/Press-Releases/` (Enforcement subset)",
        "- **Statutory Authority:**",
        "  - Section 47A(1)(c) read with Section 46(4)(i), Banking Regulation Act, 1949",
        "  - Section 58G(1)(a) read with Section 58B(5)(aa), Reserve Bank of India Act, 1934",
        "- **Role:** Monetary penalties, directions on operations (e.g. restriction on onboarding new customers), license cancellations, or compounding of FEMA violations.",
        "- **Operational Rule for Agents:** Look up penal precedents in `index/agent_router/citation_and_consequence_graph.jsonl` under the relationship `PENALIZES_UNDER`.",
        "",
        "### Tier 5: Routine Market Operations & Administrative Notices",
        "- **Primary Source:** `data/Press-Releases/` (Market Operations)",
        "- **Role:** Daily Money Market Operations, Sovereign Gold Bond issuances, Treasury Bill auction results, holiday calendars, press conferences.",
        "- **Operational Rule for Agents:** Ephemeral operational announcements. Do not cite as substantive statutory doctrine.",
        "",
        "---",
        "",
        "## 2. Deterministic Agent Retrieval Protocol (<= 3 Tool Calls)",
        "",
        "Follow these exact routes to retrieve regulations deterministically:",
        "",
        "### Route A: Lookup by Regulated Entity & Topic (Controlling Law)",
        "1. **Tool Call 1:** Read `index/agent_router/active_master_directions_by_entity.json` or `.md`.",
        "2. **Tool Call 2:** Locate the section for your entity (`Commercial Banks`, `NBFCs`, `UCBs`, `Payment Systems`, `FEMA`, etc.) and find the matching subject.",
        "3. **Tool Call 3:** Read the target `data/Master-Directions/<Year>/<file>.md`.",
        "",
        "### Route B: Lookup by RBI Circular Reference (e.g. RBI/2024-25/102 or DOR.No...)",
        "1. **Tool Call 1:** Read `index/agent_router/circular_ref_to_path.json` (or lookup target key).",
        "2. **Tool Call 2:** Retrieve the relative path `data/<Folder>/<Year>/<file>.md`.",
        "3. **Tool Call 3:** Read the document or check `index/agent_router/citation_and_consequence_graph.jsonl` for amendments/supersession.",
        "",
        "### Route C: Lookup by URL (Direct RBI URL or Hugging Face URL)",
        "1. **Tool Call 1:** Compute `shard = sha256(url.strip().lower())[:2]` (e.g. `a3`).",
        "2. **Tool Call 2:** Read `index/url_shards/<shard>.json` and get `data/<path>.md`.",
        "3. **Tool Call 3:** Read `data/<path>.md`.",
        "",
        "---",
        "",
        "## 3. Directory Structure Summary",
        "",
        "```",
        "rbi-regulatory-archive-1991-2026/",
        "├── INDEX.md                                   # Root Master Index",
        "├── llms.txt / llms-full.txt                   # LLM Entry Points",
        "├── STATE.json                                 # High-level conversion census (<500 bytes)",
        "├── index/",
        "│   ├── agent_router/",
        "│   │   ├── TRIAGE_GUIDE.md                    # This guide",
        "│   │   ├── AEO_REGULATORY_FAQ.md              # Statutory answer engine Q&A",
        "│   │   ├── active_master_directions_by_entity.md # MDs grouped by regulated entity",
        "│   │   ├── active_master_directions_by_entity.json # Machine-readable MDs by entity",
        "│   │   ├── circular_ref_to_path.json          # Circular ref -> file path",
        "│   │   └── citation_and_consequence_graph.jsonl # Causal citations & consequences",
        "│   ├── by_category/                           # Category-level indexes (6 folders)",
        "│   ├── by_year/                               # Yearly indexes (1991-2026)",
        "│   └── url_shards/                            # 256 compact URL shards (00.json..ff.json)",
        "├── data/",
        "│   ├── Master-Directions/<YYYY>/INDEX.md      # Per-directory index",
        "│   ├── Notifications/<YYYY>/INDEX.md",
        "│   ├── Master-Circulars/<YYYY>/INDEX.md",
        "│   ├── Draft-Notifications-Guidelines/<YYYY>/INDEX.md",
        "│   ├── Circulars/<YYYY>/INDEX.md",
        "│   └── Press-Releases/<YYYY>/INDEX.md",
        "└── manifest/",
        "    ├── catalog/<YYYY>.jsonl                   # Yearly sharded JSONL catalog",
        "    ├── sha256_conversion_ledger.csv           # Source of truth ledger",
        "    └── pdf_final_direct_urls.txt              # Direct RBI endpoint catalog",
        "```",
    ]

    triage_path = os.path.join(router_dir, "TRIAGE_GUIDE.md")
    with open(triage_path, "w", encoding="utf-8") as f:
        f.write("\n".join(triage_lines) + "\n")

    # 4. Generate AEO_REGULATORY_FAQ.md
    from .seo_aeo_engine import build_aeo_faq
    build_aeo_faq(repo_root)

    return {
        "circular_refs_count": len(circular_map),
        "citation_graph_edges": len(graph_records),
        "master_directions_count": len(md_rows),
        "entities_count": len(entities_map),
    }
