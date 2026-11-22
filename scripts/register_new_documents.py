#!/usr/bin/env python3
"""Register newly discovered RBI PDFs into the archive inventory.

Reads the JSON written by the crawler, downloads each new PDF once,
derives or preserves its canonical file name, caches the verified bytes
for offline conversion by runner.py, optionally backfills to Hugging Face
when HF_TOKEN is set, and appends new rows to the inventory JSONL,
conversion ledger (as PENDING), and direct-URL list.

Idempotent: re-running skips normalized URLs already present in the
inventory, ledger, or URL list. When --fail-on-all-skipped is set and
every fresh candidate failed to download, exits 1 instead of masking the
failure as zero delta.
"""

import argparse
import csv
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

LEDGER_FIELDS = [
    "file_path", "md_path", "category", "year", "listing_date",
    "headline", "document_id", "pdf_url", "hf_url", "pdf_sha256",
    "md_sha256", "status", "verification_status", "engine", "total_pages",
    "native_pages", "ocr_pages", "source", "converted_at_utc", "error",
]

_SKIP_LINES = {"press release", "reserve bank of india"}


def _looks_like_date(line):
    """True only when the whole line is a date, e.g. 'January 01, 2025'."""
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
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            return ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if len(doc) == 0:
            return ""
        text = doc[0].get_text()
        doc.close()
        return text
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


def _known_state(inventory_path, ledger_path, urls_path):
    """Return (known_norm_urls, existing_file_paths, existing_sha256)."""
    from src.rbi_pipeline.rbi_crawler import normalize_url

    known_urls = set()
    existing_paths = set()
    existing_sha256 = set()
    if inventory_path and os.path.exists(inventory_path):
        with open(inventory_path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("pdf_url"):
                    known_urls.add(normalize_url(row["pdf_url"]))
                if row.get("file_path"):
                    existing_paths.add(row["file_path"])
                if row.get("sha256"):
                    existing_sha256.add(row["sha256"].strip().lower())
    if ledger_path and os.path.exists(ledger_path):
        with open(ledger_path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("pdf_url"):
                    known_urls.add(normalize_url(row["pdf_url"]))
                if row.get("file_path"):
                    existing_paths.add(row["file_path"])
                if row.get("pdf_sha256"):
                    existing_sha256.add(row["pdf_sha256"].strip().lower())
    if urls_path and os.path.exists(urls_path):
        with open(urls_path, encoding="utf-8") as handle:
            for line in handle:
                norm = normalize_url(line)
                if norm:
                    known_urls.add(norm)
    return known_urls, existing_paths, existing_sha256


def _dedup_file_path(category, year, file_name, pdf_url, existing_paths):
    """Ensure file_path does not collide with an existing inventory entry."""
    candidate = f"{category}/{year}/{file_name}"
    if candidate not in existing_paths:
        existing_paths.add(candidate)
        return file_name, candidate
    stem = os.path.splitext(os.path.basename(urlparse(pdf_url).path))[0][:8] or "dup"
    base, ext = os.path.splitext(file_name)
    unique_name = f"{base}_{stem}{ext}"
    unique_path = f"{category}/{year}/{unique_name}"
    counter = 2
    while unique_path in existing_paths:
        unique_name = f"{base}_{stem}_{counter}{ext}"
        unique_path = f"{category}/{year}/{unique_name}"
        counter += 1
    existing_paths.add(unique_path)
    return unique_name, unique_path


def _write_report(report_out, payload):
    if not report_out:
        return
    os.makedirs(os.path.dirname(os.path.abspath(report_out)), exist_ok=True)
    with open(report_out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


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
    parser.add_argument("--pdf-cache-dir", default=".cache/sync/pdfs",
                        help="SHA-256 PDF cache dir for runner conversion")
    parser.add_argument("--report-out", default=".cache/sync/register_report.json",
                        help="JSON path for registration telemetry")
    parser.add_argument("--fail-on-all-skipped", action="store_true",
                        help="exit 1 if fresh candidates existed but all failed")
    args = parser.parse_args(argv)

    from src.rbi_pipeline.hf_enumerator import hf_resolve_url
    from src.rbi_pipeline.rbi_crawler import (
        derive_canonical_name, download_new_pdf, normalize_url, sync_new_to_hf,
    )

    discovered = _load_json(args.new_documents)
    known_urls, existing_paths, existing_sha256 = _known_state(
        args.inventory, args.ledger, args.urls_file
    )

    fresh = []
    seen_fresh = set()
    for d in discovered:
        norm = normalize_url(d.get("pdf_url"))
        if not norm or norm in known_urls or norm in seen_fresh:
            continue
        seen_fresh.add(norm)
        fresh.append(d)
    # Process RBI-sourced discoveries before HF mirror entries so RBI metadata wins.
    fresh.sort(key=lambda d: (1 if d.get("source") == "huggingface" else 0, d.get("pdf_url", "")))
    hf_mirror_paths = {
        d["file_path"].strip()
        for d in fresh
        if d.get("source") == "huggingface" and d.get("file_path")
    }
    print(f"discovered {len(discovered)}, {len(fresh)} new after dedup")

    registered = []
    to_upload = []
    skipped = []
    registered_by_sha256 = {}
    registered_by_path = {}
    dedup_hf_matched = 0
    os.makedirs(args.work_dir, exist_ok=True)
    if args.pdf_cache_dir:
        os.makedirs(args.pdf_cache_dir, exist_ok=True)

    for entry in fresh:
        pdf_url = entry["pdf_url"]
        if entry.get("source") == "huggingface" and entry.get("file_path"):
            hf_fp = entry["file_path"].strip()
            if hf_fp in registered_by_path:
                registered_by_path[hf_fp]["hf_uploaded"] = True
                dedup_hf_matched += 1
                continue
            if hf_fp in existing_paths:
                dedup_hf_matched += 1
                continue

        try:
            meta = download_new_pdf(pdf_url, args.work_dir)
        except Exception as exc:
            msg = str(exc)
            print(f"SKIP {pdf_url}: download failed: {msg}")
            skipped.append({"pdf_url": pdf_url, "reason": msg})
            continue

        sha = meta["sha256"].lower()
        if sha in registered_by_sha256:
            existing_rec = registered_by_sha256[sha]
            if entry.get("source") == "huggingface":
                existing_rec["hf_uploaded"] = True
                to_upload = [u for u in to_upload if u["sha256"].lower() != sha]
            dedup_hf_matched += 1
            continue
        if sha in existing_sha256:
            dedup_hf_matched += 1
            continue

        with open(meta["local_path"], "rb") as handle:
            pdf_bytes = handle.read()
        page_text = _page_one_text(pdf_bytes)

        if args.pdf_cache_dir:
            cached_path = os.path.join(args.pdf_cache_dir, f"{meta['sha256']}.pdf")
            shutil.copyfile(meta["local_path"], cached_path)

        # Preserve pre-named HF file_path when syncing only from Hugging Face watcher
        if entry.get("source") == "huggingface" and entry.get("file_path"):
            fp = entry["file_path"].strip()
            parts = fp.split("/")
            cat = parts[0] if len(parts) >= 3 else (entry.get("category") or "Circulars")
            yr = parts[1] if len(parts) >= 3 else str(datetime.now(timezone.utc).year)
            fname = parts[-1]
            headline = entry.get("headline") or _headline_from_page_text(page_text) or os.path.splitext(fname)[0]
            info = {
                "file_name": fname,
                "date": f"{yr}-01-01",
                "listing_date": entry.get("listing_date") or f"{yr}-01-01",
                "date_source": "hf-path",
                "document_id": entry.get("document_id") or os.path.splitext(fname)[0],
                "headline": headline,
                "category": cat,
            }
            if fp not in existing_paths:
                existing_paths.add(fp)
                file_path = fp
                file_name = fname
            else:
                file_name, file_path = _dedup_file_path(cat, yr, fname, pdf_url, existing_paths)
        else:
            crawler_headline = (entry.get("headline") or "").strip()
            headline = crawler_headline or _headline_from_page_text(page_text)
            info = derive_canonical_name(
                pdf_url,
                listing_url=entry.get("listing_url") or None,
                headline=headline or None,
                listing_date=entry.get("listing_date") or None,
                page_text=page_text,
                category=entry.get("category") or None,
                document_id=entry.get("document_id") or None,
            )
            year = info["date"][:4]
            file_name, file_path = _dedup_file_path(
                info["category"], year, info["file_name"], pdf_url, existing_paths
            )

        already_on_hf = entry.get("source") == "huggingface" or file_path in hf_mirror_paths
        year_int = int(info["date"][:4])
        rec_full = {
            "pdf_url": pdf_url,
            "listing_url": entry.get("listing_url") or "",
            "source_endpoint": entry.get("source_endpoint") or "",
            "source_endpoint_url": entry.get("source_endpoint_url") or "",
            "local_path": meta["local_path"],
            "file_name": file_name,
            "file_path": file_path,
            "category": info["category"],
            "year": year_int,
            "document_id": info["document_id"],
            "headline": info["headline"],
            "headline_source": "listing" if entry.get("headline") else ("page1" if headline else "none"),
            "listing_date": info["listing_date"],
            "date": info["date"],
            "date_source": info["date_source"],
            "bytes": meta["bytes"],
            "sha256": meta["sha256"],
            "hf_url": hf_resolve_url(file_path),
            "hf_uploaded": already_on_hf,
        }
        registered.append(rec_full)
        registered_by_sha256[sha] = rec_full
        registered_by_path[file_path] = rec_full
        existing_sha256.add(sha)
        if not already_on_hf:
            to_upload.append(rec_full)

    hf_warning = None
    if to_upload:
        uploaded, hf_warning = sync_new_to_hf(to_upload)
        if hf_warning:
            print(f"warning: {hf_warning}")
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
                    "listing_date": rec["listing_date"],
                    "listing_url": rec["listing_url"],
                    "pdf_url": rec["pdf_url"],
                    "sha256": rec["sha256"],
                    "year": rec["year"],
                }, ensure_ascii=False) + "\n")
        with open(args.ledger, "a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
            for rec in registered:
                writer.writerow({
                    "file_path": rec["file_path"],
                    "md_path": "data/" + rec["file_path"][:-4] + ".md",
                    "category": rec["category"],
                    "year": str(rec["year"]),
                    "listing_date": rec["listing_date"],
                    "headline": rec["headline"],
                    "document_id": rec["document_id"],
                    "pdf_url": rec["pdf_url"],
                    "hf_url": rec["hf_url"],
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

    # Keep sync/registered.json clean (no runner temp local_path) and skip redundant write on 0 delta
    clean_registered = [
        {k: v for k, v in rec.items() if k != "local_path"}
        for rec in registered
    ]
    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)
    should_write_out = True
    if not clean_registered and os.path.exists(args.out):
        try:
            if json.load(open(args.out, encoding="utf-8")) == []:
                should_write_out = False
        except Exception:
            pass
    if should_write_out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(clean_registered, handle, indent=2, ensure_ascii=False)

    hf_uploaded_count = sum(1 for r in registered if r.get("hf_uploaded"))
    _write_report(args.report_out, {
        "registered_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "discovered_count": len(discovered),
        "fresh_count": len(fresh),
        "registered_count": len(registered),
        "skipped_count": len(skipped),
        "dedup_hf_matched": dedup_hf_matched,
        "hf_uploaded_count": hf_uploaded_count,
        "hf_warning": hf_warning or "",
        "skipped_items": skipped,
        "registered_items": clean_registered,
    })

    print(
        f"registered {len(registered)} new documents "
        f"(skipped={len(skipped)}, dedup_hf_matched={dedup_hf_matched}, hf_uploaded={hf_uploaded_count}), "
        f"wrote {args.out}"
    )
    if args.fail_on_all_skipped and len(skipped) > 0 and len(registered) == 0:
        print(
            f"error: all {len(fresh)} fresh candidate(s) failed to download; "
            "refusing silent zero-delta pass.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
