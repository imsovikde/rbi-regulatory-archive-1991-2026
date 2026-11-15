#!/usr/bin/env python3
"""Dynamic metadata and counter synchronization engine.

Calculates live document counts, category breakdowns, year spans, and
generates SEO/AEO metadata artifacts without hardcoded static counts.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

HF_FOLDERS = [
    "Master-Directions",
    "Notifications",
    "Master-Circulars",
    "Draft-Notifications-Guidelines",
    "Circulars",
    "Press-Releases",
]

DEFAULT_BLOCKED_COUNT = 3864


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_inventory_path(repo_root: str) -> str:
    candidates = [
        os.path.join(repo_root, "manifest", "hf_inventory.jsonl"),
        os.path.join(repo_root, "manifest", "hf_88236_inventory.jsonl"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


def get_archive_metrics(repo_root: str) -> dict:
    """Read inventory, ledger, and URL manifests to compute live counts."""
    inventory_path = resolve_inventory_path(repo_root)
    ledger_path = os.path.join(repo_root, "manifest", "sha256_conversion_ledger.csv")
    urls_path = os.path.join(repo_root, "manifest", "pdf_final_direct_urls.txt")

    inventory_count = 0
    by_folder = Counter()
    by_year = Counter()
    years = set()

    if os.path.exists(inventory_path):
        with open(inventory_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                inventory_count += 1
                try:
                    row = json.loads(line)
                    folder = row.get("category") or (row.get("file_path", "").split("/")[0] if "/" in row.get("file_path", "") else "Unknown")
                    by_folder[folder] += 1
                    y = int(row.get("year", 0))
                    if y > 0:
                        by_year[y] += 1
                        years.add(y)
                except Exception:
                    pass

    done_count = 0
    by_folder_done = Counter()
    by_year_done = Counter()

    if os.path.exists(ledger_path):
        with open(ledger_path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if (row.get("status") or "").strip() == "DONE":
                    done_count += 1
                    folder = row.get("category") or (row.get("file_path", "").split("/")[0] if "/" in row.get("file_path", "") else "Unknown")
                    by_folder_done[folder] += 1
                    try:
                        y = int(row.get("year", 0))
                        if y > 0:
                            by_year_done[y] += 1
                            years.add(y)
                    except Exception:
                        pass

    direct_urls_count = 0
    if os.path.exists(urls_path):
        with open(urls_path, "r", encoding="utf-8") as f:
            direct_urls_count = sum(1 for line in f if line.strip())

    year_min = min(years) if years else 1991
    year_max = max(years) if years else 2026
    total_count = inventory_count if inventory_count > 0 else done_count
    remaining_count = max(0, total_count - done_count)
    pct = (done_count / total_count * 100.0) if total_count else 100.0

    return {
        "total_pdfs": total_count,
        "total_done": done_count,
        "total_remaining": remaining_count,
        "pct": pct,
        "year_min": year_min,
        "year_max": year_max,
        "direct_urls_count": direct_urls_count,
        "blocked_count": DEFAULT_BLOCKED_COUNT,
        "census_total": total_count + DEFAULT_BLOCKED_COUNT,
        "by_folder": dict(by_folder),
        "by_folder_done": dict(by_folder_done),
        "by_year": dict(by_year),
        "by_year_done": dict(by_year_done),
    }


def build_schema_org_jsonld(repo_root: str, metrics: dict | None = None) -> str:
    """Generate Schema.org Dataset and Legislation JSON-LD manifest."""
    metrics = metrics or get_archive_metrics(repo_root)
    seo_dir = os.path.join(repo_root, "seo")
    os.makedirs(seo_dir, exist_ok=True)
    out_path = os.path.join(seo_dir, "schema_org_dataset.jsonld")

    dataset_jsonld = {
        "@context": "https://schema.org",
        "@type": ["Dataset", "Legislation"],
        "name": f"Reserve Bank of India (RBI) Regulatory Archive 1991-{metrics['year_max']}",
        "alternateName": "RBI Regulatory Markdown Archive",
        "description": (
            f"Agent-first Markdown index for the Reserve Bank of India Regulatory Archive (1991-{metrics['year_max']}). "
            f"{metrics['total_done']:,}/{metrics['total_pdfs']:,} regulatory PDFs converted to GitHub-Flavored Markdown "
            f"with SHA-256 verification, statutory graph routing, and llms.txt."
        ),
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
        "temporalCoverage": f"{metrics['year_min']}-01-01/{metrics['year_max']}-12-31",
        "spatialCoverage": "India",
        "jurisdiction": "Reserve Bank of India",
        "inLanguage": ["en", "hi"],
        "variableMeasured": [
            {
                "@type": "PropertyValue",
                "name": "total_documents",
                "value": metrics["total_pdfs"],
            },
            {
                "@type": "PropertyValue",
                "name": "converted_documents",
                "value": metrics["total_done"],
            },
            {
                "@type": "PropertyValue",
                "name": "census_total",
                "value": metrics["census_total"],
            },
            {
                "@type": "PropertyValue",
                "name": "direct_rbi_urls",
                "value": metrics["direct_urls_count"],
            },
        ],
        "distribution": [
            {
                "@type": "DataDownload",
                "encodingFormat": "text/markdown",
                "contentUrl": "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026",
            },
            {
                "@type": "DataDownload",
                "encodingFormat": "application/pdf",
                "contentUrl": "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026",
            },
        ],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset_jsonld, f, indent=2)

    return out_path


def build_sitemap_index(repo_root: str, metrics: dict | None = None) -> str:
    """Generate seo/sitemap_index.xml listing category and yearly indexes."""
    metrics = metrics or get_archive_metrics(repo_root)
    seo_dir = os.path.join(repo_root, "seo")
    os.makedirs(seo_dir, exist_ok=True)
    out_path = os.path.join(seo_dir, "sitemap_index.xml")

    base_url = "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/blob/main"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urls = [
        f"{base_url}/README.md",
        f"{base_url}/INDEX.md",
        f"{base_url}/llms.txt",
        f"{base_url}/llms-full.txt",
        f"{base_url}/index/agent_router/TRIAGE_GUIDE.md",
        f"{base_url}/index/agent_router/AEO_REGULATORY_FAQ.md",
        f"{base_url}/index/agent_router/active_master_directions_by_entity.md",
    ]

    for cat in HF_FOLDERS:
        urls.append(f"{base_url}/index/by_category/{cat}.md")

    for y in sorted(metrics.get("by_year", {}).keys()):
        urls.append(f"{base_url}/index/by_year/{y}.md")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("    <changefreq>weekly</changefreq>")
        lines.append("  </url>")
    lines.append("</urlset>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return out_path


def sync_github_repo_metadata(repo_root: str, metrics: dict | None = None) -> bool:
    """Update GitHub repository description and topics using gh repo edit."""
    metrics = metrics or get_archive_metrics(repo_root)
    desc = (
        f"Agent-first Markdown index for the RBI Regulatory Archive (1991-{metrics['year_max']}). "
        f"{metrics['total_done']:,}/{metrics['total_pdfs']:,} RBI PDFs "
        f"(Master Directions, Notifications, Master Circulars, Drafts, Circulars, Press Releases) "
        f"mirrored from Hugging Face with SHA-256 verification and llms.txt."
    )
    topics = [
        "rbi", "reserve-bank-of-india", "indian-law", "banking-regulation",
        "markdown-archive", "llms-txt", "legal-tech", "mcp", "rag-dataset",
    ]
    cmd = [
        "gh", "repo", "edit", "imsovikde/rbi-regulatory-archive-1991-2026",
        "--description", desc,
    ]
    for t in topics:
        cmd.extend(["--add-topic", t])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return res.returncode == 0
    except Exception as exc:
        print(f"warning: gh repo edit failed: {exc}", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    metrics = get_archive_metrics(repo_root)
    print(f"Live archive metrics: {metrics['total_done']}/{metrics['total_pdfs']} ({metrics['pct']:.4f}%)")

    jsonld_path = build_schema_org_jsonld(repo_root, metrics)
    print(f"Generated Schema.org JSON-LD: {jsonld_path}")

    sitemap_path = build_sitemap_index(repo_root, metrics)
    print(f"Generated Sitemap XML: {sitemap_path}")

    synced = sync_github_repo_metadata(repo_root, metrics)
    print(f"GitHub repository description synced: {synced}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
