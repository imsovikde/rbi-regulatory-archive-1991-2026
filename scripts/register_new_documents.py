#!/usr/bin/env python3
"""Register newly discovered RBI PDFs into the archive inventory.

Reads the JSON written by the crawler
(``python3 -m src.rbi_pipeline.rbi_crawler --urls ... --ledger ... --out
.cache/sync/new_documents.json``), downloads each new PDF once, derives
its canonical file name, and appends it to the inventory JSONL, the
conversion ledger (as PENDING), and the direct-URL list. When HF_TOKEN
is set, the PDFs are also backfilled to the Hugging Face dataset first
(PDFs are never invented: only files actually served by RBI are
registered). The runner then converts the new pending rows on its
normal pass, so no separate conversion mode is needed.

Headline rule: the listing page is not recorded by the crawler, so the
headline is taken from the PDF's own page 1 (first substantial line
after the masthead), falling back to NO_HEADLINE. The date comes from
page 1 when found, else today. Both are recorded in the output JSON
with their source, so a human can correct them later. Known limit: the
document ID for a new press release is the PDF file stem (a hash),
not the numeric listing ID, because the crawler does not record the
item display page; the file is still uniquely named, converted, and
indexed.

Idempotent: re-running with the same input skips URLs already present
in the inventory or ledger. Exit 0 always (0 new documents is normal).
"""

import argparse
import csv
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import quote

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

LEDGER_FIELDS = [
    "file_path", "md_path", "category", "year", "listing_date",
    "headline", "document_id", "pdf_url", "hf_url", "pdf_sha256",
    "md_sha256", "status", "verification_status", "engine", "total_pages",
    "native_pages", "ocr_pages", "source", "converted_at_utc", "error",
]
HF_DATASET = "imsovikde/rbi-regulatory-archive-1991-2026"
HF_BASE = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/"

_SKIP_LINES = {"press release", "reserve bank of india"}


def _looks_like_date(line):
    """True only when the whole line is a date, e.g. 'January 01, 2025'.

    A headline that merely contains a date ("Money Market Operations as
    on December 31, 2024") must NOT be rejected.
    """
    import re

    stripped = line.strip()
    months = (
        "January|February|March|April|May|June|July|August|September|"
        "October|November|December"
    )
    return bool(re.fullmatch(
        rf"(?:{months})\s+\d{{1,2}},?\s+\d{{4}}"
        rf"|\d{{1,2}}\s+(?:{months})\s+\d{{4}}"
        rf"|\d{{4}}-\d{{2}}-\d{{2}}",
        stripped,
    ))


def _page_one_text(pdf_bytes):
    """Text of page 1, or '' when PyMuPDF is unavailable."""
    try:
        import fitz
    except ImportError:
        return ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if len(doc) == 0:
            return ""
        return doc[0].get_text()
    except Exception:
        return ""


def _headline_from_page_text(text):
    """First substantial line of page 1, skipping the masthead."""
    for line in (text or "").splitlines():
        stripped = line.strip()
        if len(stripped) < 12:
            continue
        if stripped.lower() in _SKIP_LINES:
            continue
        if _looks_like_date(stripped):
            continue
        if stripped.startswith("("):
            continue
        if len(stripped.split()) < 4:
            continue
        return stripped[:120]
    return ""


def _load_json(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else []


def _known_urls(inventory_path, ledger_path, urls_path):
    known = set()
    if inventory_path and os.path.exists(inventory_path):
        with open(inventory_path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("pdf_url"):
                    known.add(row["pdf_url"])
    if ledger_path and os.path.exists(ledger_path):
        with open(ledger_path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("pdf_url"):
                    known.add(row["pdf_url"])
    if urls_path and os.path.exists(urls_path):
        with open(urls_path, encoding="utf-8") as handle:
            known.update(line.strip() for line in handle if line.strip())
    return known


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--new-documents", required=True,
                        help="JSON list from the crawler discover step")
    parser.add_argument("--inventory", required=True,
                        help="manifest/hf_88236_inventory.jsonl")
    parser.add_argument("--ledger", required=True,
                        help="manifest/sha256_conversion_ledger.csv")
    parser.add_argument("--urls-file", required=True,
                        help="manifest/pdf_final_direct_urls.txt")
    parser.add_argument("--out", required=True,
                        help="output JSON for registered documents")
    parser.add_argument("--work-dir", default=".cache/sync",
                        help="temp dir for downloaded PDFs")
    args = parser.parse_args(argv)

    from src.rbi_pipeline.rbi_crawler import (
        derive_canonical_name, download_new_pdf, sync_new_to_hf,
    )

    discovered = _load_json(args.new_documents)
    known = _known_urls(args.inventory, args.ledger, args.urls_file)
    fresh = [d for d in discovered if d.get("pdf_url") not in known]
    print(f"discovered {len(discovered)}, {len(fresh)} new after dedup")

    registered = []
    to_upload = []
    os.makedirs(args.work_dir, exist_ok=True)
    for entry in fresh:
        pdf_url = entry["pdf_url"]
        try:
            meta = download_new_pdf(pdf_url, args.work_dir)
        except Exception as exc:
            print(f"SKIP {pdf_url}: download failed: {exc}")
            continue
        with open(meta["local_path"], "rb") as handle:
            pdf_bytes = handle.read()
        page_text = _page_one_text(pdf_bytes)
        headline = _headline_from_page_text(page_text)
        info = derive_canonical_name(
            pdf_url, headline=headline or None, page_text=page_text,
            category=entry.get("category") or None,
        )
        year = info["date"][:4]
        file_path = f"{info['category']}/{year}/{info['file_name']}"
        registered.append({
            "pdf_url": pdf_url,
            "local_path": meta["local_path"],
            "file_name": info["file_name"],
            "file_path": file_path,
            "category": info["category"],
            "document_id": info["document_id"],
            "headline": info["headline"],
            "headline_source": "page1" if headline else "none",
            "date": info["date"],
            "date_source": info["date_source"],
            "bytes": meta["bytes"],
            "sha256": meta["sha256"],
            "hf_uploaded": False,
        })
        to_upload.append(registered[-1])

    if to_upload:
        uploaded, warning = sync_new_to_hf(to_upload)
        if warning:
            print(f"warning: {warning}")
        for item in uploaded:
            for rec in registered:
                if rec["pdf_url"] == item["pdf_url"]:
                    rec["hf_uploaded"] = bool(item.get("hf_uploaded"))

    if registered:
        with open(args.inventory, "a", encoding="utf-8") as handle:
            for rec in registered:
                handle.write(json.dumps({
                    "bytes": rec["bytes"],
                    "category": rec["category"],
                    "document_id": rec["document_id"],
                    "file_name": rec["file_name"],
                    "file_path": rec["file_path"],
                    "headline": rec["headline"],
                    "listing_date": rec["date"],
                    "listing_url": "",
                    "pdf_url": rec["pdf_url"],
                    "sha256": rec["sha256"],
                    "year": int(rec["date"][:4]),
                }, ensure_ascii=False) + "\n")
        with open(args.ledger, "a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
            for rec in registered:
                writer.writerow({
                    "file_path": rec["file_path"],
                    "md_path": "data/" + rec["file_path"][:-4] + ".md",
                    "category": rec["category"],
                    "year": rec["date"][:4],
                    "listing_date": rec["date"],
                    "headline": rec["headline"],
                    "document_id": rec["document_id"],
                    "pdf_url": rec["pdf_url"],
                    "hf_url": HF_BASE + quote(rec["file_path"]),
                    "pdf_sha256": rec["sha256"],
                    "md_sha256": "",
                    "status": "PENDING",
                    "verification_status": "",
                    "engine": "",
                    "total_pages": "",
                    "native_pages": "",
                    "ocr_pages": "",
                    "source": "",
                    "converted_at_utc": "",
                    "error": "",
                })
        with open(args.urls_file, "a", encoding="utf-8") as handle:
            for rec in registered:
                handle.write(rec["pdf_url"] + "\n")

    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(registered, handle, indent=2, ensure_ascii=False)
    print(f"registered {len(registered)} new documents, wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
