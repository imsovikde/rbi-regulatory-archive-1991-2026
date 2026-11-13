"""Rebuild every agent-first index for the RBI Regulatory Archive.

Reads the conversion ledger (what has been converted) plus the full
inventory (what exists) and writes, deterministically:

- llms.txt and llms-full.txt (repository root)
- INDEX.md (repository root, master table of contents)
- index/by_category/<Folder>.md (one per HF folder)
- index/by_year/<YYYY>.md and index/by_year/<YYYY>.json (1991-2026)
- index/url_to_path_map.json (any RBI or HF URL -> data/<path>.md)
- manifest/catalog/<YYYY>.jsonl (one JSON object per inventory row, one
  shard per year; sharded because a single catalog file passed GitHub's
  100 MB push limit at 60,647 rows / 103.40 MB and killed run 43443272509,
  Defect 7; the largest shard is Press-Releases 2017 at ~6.5 MB)
- README.md progress section (between markers, updated in place)
- PROGRESS.md (created with a header if missing; batch lines are appended
  by :func:`append_progress_log`, never by build_all, so rebuilds stay
  byte-identical)

Determinism: every output is written from sorted inputs with sorted keys
and stable ordering, so repeated runs over unchanged inputs produce
identical bytes. No timestamps are embedded in rebuilt files; the only
timestamps live in PROGRESS.md append-only log lines, which are not
rebuilt.

No em dashes are used in any generated file (commas and hyphens only).
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter, defaultdict

__all__ = [
    "append_progress_log",
    "build_all",
    "folder_of",
    "md_path_for",
    "progress_bar",
    "update_readme_progress",
]

PROGRESS_START = "<!-- PROGRESS-START -->"
PROGRESS_END = "<!-- PROGRESS-END -->"

HF_FOLDERS = [
    "Master-Directions",
    "Notifications",
    "Master-Circulars",
    "Draft-Notifications-Guidelines",
    "Circulars",
    "Press-Releases",
]

REPO_URL = "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026"
HF_DATASET_URL = (
    "https://huggingface.co/datasets/"
    "imsovikde/rbi-regulatory-archive-1991-2026"
)


def md_path_for(file_path):
    """Map a PDF path like ``Press-Releases/2002/x.pdf`` to its .md path.

    Returns ``data/Press-Releases/2002/x.md``. The stem is never renamed.
    """
    stem = file_path[:-4] if file_path.lower().endswith(".pdf") else file_path
    return "data/" + stem + ".md"


def progress_bar(pct, width=40):
    """ASCII progress bar, e.g. ``[####------] 12.3400%``."""
    filled = int(round(width * max(0.0, min(100.0, pct)) / 100.0))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"


def _write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _read_ledger_rows(ledger_path):
    """Read ledger CSV rows into a dict keyed by file_path."""
    rows = {}
    if not ledger_path or not os.path.exists(ledger_path):
        return rows
    with open(ledger_path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row.get("file_path") or "").strip()
            if key:
                rows[key] = row
    return rows


def folder_of(row):
    """Return the HF folder name for an inventory row.

    Authoritative source is the first segment of file_path
    ("Press-Releases/2002/..."). Falls back to the category-to-folder
    map for rows without a file_path, because the manifest category label
    ("Press-Release") differs from the folder name ("Press-Releases").
    """
    from .hf_enumerator import CATEGORY_TO_FOLDER

    path = (row.get("file_path") or "").strip()
    if "/" in path:
        return path.split("/")[0]
    category = (row.get("category") or "").strip()
    return CATEGORY_TO_FOLDER.get(category, category)


def _counts(inventory_rows, ledger_by_path):
    """Per-folder and per-year (total, done) counts from inventory + ledger."""
    by_folder = Counter()
    by_folder_done = Counter()
    by_year = Counter()
    by_year_done = Counter()
    for row in inventory_rows:
        folder = folder_of(row)
        year = row.get("year") or 0
        by_folder[folder] += 1
        by_year[year] += 1
        status = (ledger_by_path.get(row["file_path"], {}).get("status") or "")
        if status == "DONE":
            by_folder_done[folder] += 1
            by_year_done[year] += 1
    return by_folder, by_folder_done, by_year, by_year_done


def _summary_block(total, done, by_folder, by_folder_done):
    """Shared Markdown progress summary used by README and INDEX."""
    pct = (done / total * 100.0) if total else 0.0
    lines = [
        "## Conversion progress",
        "",
        f"- **Total PDFs:** {total}",
        f"- **Converted to Markdown:** {done}",
        f"- **Remaining:** {total - done}",
        f"- **Progress:** {progress_bar(pct)} {pct:.4f}%",
        "",
        "| Category | Total | Converted | Progress |",
        "| --- | ---: | ---: | ---: |",
    ]
    for folder in HF_FOLDERS:
        total_f = by_folder.get(folder, 0)
        done_f = by_folder_done.get(folder, 0)
        pct_f = (done_f / total_f * 100.0) if total_f else 0.0
        lines.append(
            f"| {folder} | {total_f} | {done_f} | {pct_f:.4f}% |"
        )
    lines.append("")
    return "\n".join(lines), pct


def update_readme_progress(repo_root, total, done, by_folder, by_folder_done):
    """Replace the README.md section between the PROGRESS markers.

    If README.md does not exist, a minimal one is created. If the markers
    are missing, the section is appended at the end. Returns the README
    path written.
    """
    summary, _pct = _summary_block(total, done, by_folder, by_folder_done)
    section = f"{PROGRESS_START}\n{summary}{PROGRESS_END}\n"
    readme_path = os.path.join(repo_root, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as handle:
            text = handle.read()
        if PROGRESS_START in text and PROGRESS_END in text:
            before, rest = text.split(PROGRESS_START, 1)
            _middle, after = rest.split(PROGRESS_END, 1)
            text = before + section + after.lstrip("\n")
            if not text.endswith("\n"):
                text += "\n"
        else:
            if text and not text.endswith("\n"):
                text += "\n"
            text += "\n" + section
    else:
        text = (
            "# RBI Regulatory Archive 1991-2026\n\n"
            "Agent-first Markdown conversion of every Reserve Bank of India "
            "regulatory PDF, 1991-2026. Source PDFs live on Hugging Face; "
            "this repository holds the converted Markdown and the indexes.\n\n"
            + section
        )
    _write(readme_path, text)
    return readme_path


def append_progress_log(repo_root, line):
    """Append one line to PROGRESS.md (append-only batch log).

    Creates PROGRESS.md with a header when missing. The line is stored
    verbatim with a trailing newline; callers supply their own timestamp.
    """
    path = os.path.join(repo_root, "PROGRESS.md")
    if not os.path.exists(path):
        _write(
            path,
            "# Conversion progress log\n\n"
            "One line per committed batch, newest at the end.\n\n",
        )
    with open(path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line.rstrip("\n") + "\n")
    return path


def _build_llms_txt(repo_root, total, done, by_folder, by_folder_done):
    summary, pct = _summary_block(total, done, by_folder, by_folder_done)
    lines = [
        "# RBI Regulatory Archive 1991-2026 - llms.txt",
        "",
        "Agent entry point. Every RBI regulatory PDF, 1991-2026, converted "
        "to GitHub-Flavored Markdown. PDFs are the source of truth and live "
        "on Hugging Face; this repository holds the Markdown and indexes.",
        "",
        f"Total PDFs: {total}. Converted: {done} ({pct:.4f}%).",
        f"Dataset: {HF_DATASET_URL}",
        "",
        "## Indexes",
        "",
        "- Master index: INDEX.md",
        "- URL lookup (any RBI or Hugging Face URL to .md path): "
        "index/url_to_path_map.json",
        "- Full catalog (one JSON object per document, one shard per "
        "year): manifest/catalog/<YYYY>.jsonl",
        "",
        "## Categories",
        "",
    ]
    for folder in HF_FOLDERS:
        lines.append(
            f"- {folder}: {by_folder_done.get(folder, 0)}/"
            f"{by_folder.get(folder, 0)} converted, "
            f"index/by_category/{folder}.md"
        )
    lines += [
        "",
        "## Years",
        "",
        "Per-year indexes: index/by_year/<YYYY>.md and "
        "index/by_year/<YYYY>.json for 1991 through 2026.",
        "",
        "## How to find a document",
        "",
        "1. If you have an RBI URL, look it up in "
        "index/url_to_path_map.json to get the data/<path>.md file.",
        "2. If you have a category and year, open the matching "
        "index/by_year/<YYYY>.md table.",
        "3. Converted Markdown lives under data/<Folder>/<Year>/ with the "
        "exact PDF stem and a .md extension.",
        "",
    ]
    _write(os.path.join(repo_root, "llms.txt"), "\n".join(lines))


def _build_llms_full_txt(repo_root, by_year, by_year_done):
    lines = [
        "# RBI Regulatory Archive 1991-2026 - llms-full.txt",
        "",
        "Exhaustive agent directory. Every category index and every yearly "
        "index, with conversion counts.",
        "",
        "## Category indexes",
        "",
    ]
    for folder in HF_FOLDERS:
        lines.append(f"- index/by_category/{folder}.md")
    lines += ["", "## Yearly indexes", ""]
    for year in sorted(by_year):
        lines.append(
            f"- {year}: {by_year_done.get(year, 0)}/{by_year[year]} "
            f"converted, index/by_year/{year}.md, index/by_year/{year}.json"
        )
    lines.append("")
    _write(os.path.join(repo_root, "llms-full.txt"), "\n".join(lines))


def _build_root_index(repo_root, total, done, by_folder, by_folder_done,
                      by_year, by_year_done):
    summary, _pct = _summary_block(total, done, by_folder, by_folder_done)
    lines = [
        "# RBI Regulatory Archive 1991-2026 - Index",
        "",
        summary,
        "## Categories",
        "",
        "| Category | Index |",
        "| --- | --- |",
    ]
    for folder in HF_FOLDERS:
        lines.append(f"| {folder} | [index](index/by_category/{folder}.md) |")
    lines += ["", "## Years", "", "| Year | Total | Converted | Index |",
              "| ---: | ---: | ---: | --- |"]
    for year in sorted(by_year):
        lines.append(
            f"| {year} | {by_year[year]} | {by_year_done.get(year, 0)} | "
            f"[index](index/by_year/{year}.md) |"
        )
    lines.append("")
    _write(os.path.join(repo_root, "INDEX.md"), "\n".join(lines))


def _build_category_indexes(repo_root, inventory_rows, ledger_by_path):
    from .hf_enumerator import hf_resolve_url

    by_folder_rows = defaultdict(list)
    for row in inventory_rows:
        by_folder_rows[folder_of(row)].append(row)
    for folder in HF_FOLDERS:
        rows = sorted(
            by_folder_rows.get(folder, []),
            key=lambda r: (r["year"], r["file_name"]),
        )
        done = sum(
            1
            for r in rows
            if (ledger_by_path.get(r["file_path"], {}).get("status") or "")
            == "DONE"
        )
        lines = [
            f"# {folder}",
            "",
            f"Total: {len(rows)}. Converted: {done}.",
            "",
            "Converted documents link to their Markdown file under "
            "data/. Pending documents link to the source PDF on Hugging "
            "Face.",
            "",
            "| Year | Headline | Document | Status |",
            "| ---: | --- | --- | --- |",
        ]
        for row in rows:
            md_path = md_path_for(row["file_path"])
            status = (
                ledger_by_path.get(row["file_path"], {}).get("status") or ""
            )
            if status == "DONE":
                link = f"[Markdown](../{md_path})"
                status_text = "DONE"
            else:
                link = f"[PDF]({hf_resolve_url(row['file_path'])})"
                status_text = "PENDING"
            headline = (row.get("headline") or "").replace("|", "\\|")
            lines.append(
                f"| {row['year']} | {headline} | {link} | {status_text} |"
            )
        lines.append("")
        _write(
            os.path.join(repo_root, "index", "by_category", folder + ".md"),
            "\n".join(lines),
        )


def _build_year_indexes(repo_root, inventory_rows, ledger_by_path):
    from .hf_enumerator import hf_resolve_url

    by_year_rows = defaultdict(list)
    for row in inventory_rows:
        by_year_rows[row.get("year") or 0].append(row)
    for year in sorted(by_year_rows):
        rows = sorted(
            by_year_rows[year], key=lambda r: (folder_of(r), r["file_name"])
        )
        lines = [
            f"# RBI Regulatory Archive - {year}",
            "",
            f"Total: {len(rows)} documents.",
            "",
            "| Category | Headline | Document | Status |",
            "| --- | --- | --- | --- |",
        ]
        json_docs = []
        for row in rows:
            status = (
                ledger_by_path.get(row["file_path"], {}).get("status") or ""
            )
            is_done = status == "DONE"
            md_path = md_path_for(row["file_path"])
            if is_done:
                link = f"[Markdown](../../{md_path})"
                status_text = "DONE"
            else:
                link = f"[PDF]({hf_resolve_url(row['file_path'])})"
                status_text = "PENDING"
            headline = (row.get("headline") or "").replace("|", "\\|")
            lines.append(
                f"| {row.get('folder') or ''} | {headline} | {link} | "
                f"{status_text} |"
            )
            json_docs.append({
                "category": row.get("category") or "",
                "folder": folder_of(row),
                "year": year,
                "listing_date": row.get("listing_date") or "",
                "headline": row.get("headline") or "",
                "document_id": row.get("document_id") or "",
                "listing_url": row.get("listing_url") or "",
                "pdf_url": row.get("pdf_url") or "",
                "file_path": row["file_path"],
                "md_path": md_path if is_done else None,
                "pdf_sha256": row.get("sha256") or "",
                "status": status if status else "PENDING",
            })
        lines.append("")
        _write(
            os.path.join(repo_root, "index", "by_year", f"{year}.md"),
            "\n".join(lines),
        )
        _write(
            os.path.join(repo_root, "index", "by_year", f"{year}.json"),
            json.dumps(
                {"year": year, "total": len(rows), "documents": json_docs},
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            + "\n",
        )


def _build_url_map(repo_root, inventory_rows):
    from .hf_enumerator import hf_resolve_url

    mapping = {}
    for row in inventory_rows:
        md_path = md_path_for(row["file_path"])
        pdf_url = (row.get("pdf_url") or "").strip()
        if pdf_url:
            mapping[pdf_url] = md_path
        mapping[hf_resolve_url(row["file_path"])] = md_path
    _write(
        os.path.join(repo_root, "index", "url_to_path_map.json"),
        json.dumps(mapping, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n",
    )


def _build_master_catalog(repo_root, inventory_rows, ledger_by_path):
    """Write the machine-readable catalog, sharded one file per year.

    One JSON object per inventory row, same record shape as before
    (sorted keys, UTF-8, LF newlines). The shards live in
    ``manifest/catalog/<YYYY>.jsonl``.

    Sharding is not cosmetic. The catalog used to be a single file,
    ``manifest/master_catalog.jsonl``; it grows by ~1.7 KB per row and
    passed GitHub's hard 100 MB per-file push limit at 60,647 rows
    (103.40 MB), which rejected the graceful-stop index commit and
    killed run 43443272509 (Defect 7). A single Press-Releases shard
    would still exceed the limit (~109 MB), so the split is by year:
    the largest year (Press-Releases 2017, 3,836 files) is ~6.5 MB.
    The old single file is NOT written or deleted here; it was removed
    from the repo once, by hand, when this fix landed.
    """
    from .hf_enumerator import hf_resolve_url

    by_year_rows = defaultdict(list)
    for row in inventory_rows:
        try:
            year = int(row.get("year") or 0)
        except (TypeError, ValueError):
            year = 0
        by_year_rows[year].append(row)
    catalog_dir = os.path.join(repo_root, "manifest", "catalog")
    os.makedirs(catalog_dir, exist_ok=True)
    for year in sorted(by_year_rows):
        path = os.path.join(catalog_dir, f"{year:04d}.jsonl")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            for row in by_year_rows[year]:
                ledger = ledger_by_path.get(row["file_path"], {})
                status = ledger.get("status") or ""
                record = {
                    "category": row.get("category") or "",
                    "folder": folder_of(row),
                    "year": row.get("year") or 0,
                    "listing_date": row.get("listing_date") or "",
                    "headline": row.get("headline") or "",
                    "document_id": row.get("document_id") or "",
                    "listing_url": row.get("listing_url") or "",
                    "pdf_url": row.get("pdf_url") or "",
                    "hf_url": hf_resolve_url(row["file_path"]),
                    "file_path": row["file_path"],
                    "md_path": md_path_for(row["file_path"]),
                    "pdf_sha256": row.get("sha256") or "",
                    "md_sha256": ledger.get("md_sha256") or None,
                    "status": status if status else "PENDING",
                    "engine": ledger.get("engine") or None,
                    "total_pages": ledger.get("total_pages") or None,
                    "native_pages": ledger.get("native_pages") or None,
                    "ocr_pages": ledger.get("ocr_pages") or None,
                    "converted_at_utc": ledger.get("converted_at_utc") or None,
                }
                handle.write(
                    json.dumps(record, sort_keys=True, ensure_ascii=False)
                    + "\n"
                )


def build_all(repo_root, ledger_rows, inventory_rows):
    """Rebuild every index from ledger rows and inventory rows.

    ``ledger_rows`` is a list of ledger dicts (as read from
    manifest/sha256_conversion_ledger.csv, or as built in memory by the
    runner). ``inventory_rows`` is a list of dicts in the
    :func:`hf_enumerator.iter_inventory` shape, in manifest order.

    Returns a dict of counts: total, done, remaining, pct.
    """
    ledger_by_path = {}
    for row in ledger_rows:
        key = (row.get("file_path") or "").strip()
        if key:
            ledger_by_path[key] = row
    total = len(inventory_rows)
    done = sum(
        1
        for row in inventory_rows
        if (ledger_by_path.get(row["file_path"], {}).get("status") or "")
        == "DONE"
    )
    by_folder, by_folder_done, by_year, by_year_done = _counts(
        inventory_rows, ledger_by_path
    )
    _build_llms_txt(repo_root, total, done, by_folder, by_folder_done)
    _build_llms_full_txt(repo_root, by_year, by_year_done)
    _build_root_index(
        repo_root, total, done, by_folder, by_folder_done,
        by_year, by_year_done,
    )
    _build_category_indexes(repo_root, inventory_rows, ledger_by_path)
    _build_year_indexes(repo_root, inventory_rows, ledger_by_path)
    _build_url_map(repo_root, inventory_rows)
    _build_master_catalog(repo_root, inventory_rows, ledger_by_path)
    update_readme_progress(repo_root, total, done, by_folder, by_folder_done)
    return {
        "total": total,
        "done": done,
        "remaining": total - done,
        "pct": (done / total * 100.0) if total else 0.0,
    }
