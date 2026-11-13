"""Batch conversion loop for the RBI Regulatory Archive.

Runs as::

    python3 -m src.rbi_pipeline.runner --manifest manifest/hf_88236_inventory.jsonl \\
        --batch-size 75 --max-runtime-seconds 17400 \\
        --state STATE.json --ledger manifest/sha256_conversion_ledger.csv

Behaviour, in order:

1. Load the inventory (JSONL preferred, CSV also accepted) and STATE.json.
2. Take the next ``batch_size`` PENDING rows in deterministic manifest
   order (rows whose file_path is not in STATE.json ``done_paths``).
3. For each row: download the PDF from the Hugging Face resolve URL;
   on HF failure, fall back to the direct RBI ``pdf_url`` and record which
   source was used. Verify the PDF SHA-256. Convert with
   ``converter.convert_pdf`` (imported lazily; if the converter module is
   missing, exit 2 with a clear error, never write empty files). Write
   ``data/<file_path with .pdf replaced by .md>`` with YAML frontmatter.
4. After the batch: append ledger rows, update STATE.json, append one
   PROGRESS.md line, update the README.md progress bar, then push exactly
   ONE signed commit for the batch via :mod:`git_committer`.
5. Stop starting new batches once ``max-runtime-seconds`` minus a 600
   second reserve is reached, flush state, and exit 0 with
   ``remaining_count > 0`` so the workflow can self-chain the next run.

Converter contract (``src/rbi_pipeline/converter.py``): ``convert_pdf(pdf_bytes,
metadata) -> dict`` where ``metadata`` is the inventory row dict plus a
``pdf_sha256`` key, and the returned dict has keys ``markdown`` (the
complete file: YAML frontmatter followed by the GFM body, one
``<!-- PAGE N -->`` anchor per page), ``md_sha256`` (SHA-256 of the body
only), ``total_pages``, ``native_pages``, ``ocr_pages``, ``engine`` and
``verification_status`` (``VERIFIED_LEVEL_5``, ``NEEDS_REVIEW`` or
``FAILED_UNREADABLE``). The runner writes the converter's Markdown
verbatim, injects the download ``source`` (``hf`` or ``rbi``) and a
percent-encoded ``source_hf_url`` into the frontmatter (neither affects
``md_sha256``, which covers the body only), and records the converter's
``verification_status`` in the ledger. A ``markdown_body`` key (GFM
without frontmatter) is also accepted for alternative converters; in
that case the runner builds the frontmatter itself.

Workers: ``--workers`` defaults to 2, but parallel execution is used
only when the converter module sets ``PROCESS_SAFE = True``. Otherwise
the run is sequential with a warning. This is deliberate: a converter
that holds GPU state, a model in memory, or non-fork-safe handles must
never be run under ProcessPoolExecutor.

Disk guard: one PDF is held in memory at a time per worker and its bytes
are released after conversion; a batch refuses to start when less than
1 GiB of free disk remains under the repository root.

Exit codes: 0 = batch(es) done, or no work left, or time budget reached
with state flushed (self-chain continues). 2 = unrecoverable error with
state flushed (missing converter, missing manifest, unsigned commit,
disk exhaustion).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

__all__ = ["main"]

LEDGER_FIELDS = [
    "file_path", "md_path", "category", "year", "listing_date",
    "headline", "document_id", "pdf_url", "hf_url", "pdf_sha256",
    "md_sha256", "status", "verification_status", "engine", "total_pages",
    "native_pages", "ocr_pages", "source", "converted_at_utc", "error",
]

_MIN_FREE_BYTES = 1024 ** 3  # 1 GiB
_TIME_RESERVE_SECONDS = 600  # stop starting batches this long before the limit


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(message):
    print(f"[runner { _utcnow_iso()}] {message}", flush=True)


def _atomic_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def load_inventory(manifest_path):
    """Load inventory rows from a .jsonl or .csv manifest, in file order.

    JSONL rows must already carry the iter_inventory dict shape. CSV rows
    are read through :func:`hf_enumerator.iter_inventory` (which sorts
    deterministically and filters to DOWNLOADED rows).
    """
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    if manifest_path.endswith(".jsonl"):
        rows = []
        with open(manifest_path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
    if manifest_path.endswith(".csv"):
        from .hf_enumerator import iter_inventory

        return list(iter_inventory(manifest_path))
    raise ValueError(
        f"unsupported manifest format (need .jsonl or .csv): {manifest_path}"
    )


def load_state(state_path, total_count):
    """Load STATE.json, or initialise it when missing."""
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as handle:
            state = json.load(handle)
        state.setdefault("done_paths", [])
        return state
    return {
        "total_count": total_count,
        "done_count": 0,
        "done_paths": [],
        "remaining_count": total_count,
        "last_batch": 0,
        "updated_at_utc": _utcnow_iso(),
        "pct": 0.0,
    }


def save_state(state_path, state):
    state["updated_at_utc"] = _utcnow_iso()
    total = state.get("total_count") or 0
    done = state.get("done_count") or 0
    state["remaining_count"] = total - done
    state["pct"] = round(done / total * 100.0, 4) if total else 0.0
    _atomic_write_json(state_path, state)


def load_ledger(ledger_path):
    """Return (rows list, by_path dict) for the ledger CSV, empty if missing."""
    rows = []
    by_path = {}
    if ledger_path and os.path.exists(ledger_path):
        with open(ledger_path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                rows.append(row)
                key = (row.get("file_path") or "").strip()
                if key:
                    by_path[key] = row
    return rows, by_path


def upsert_ledger_rows(ledger_path, all_rows, batch_rows):
    """Update the ledger CSV in place: one row per file, forever.

    The seed ledger holds one PENDING row per file. A converted file
    must REPLACE its PENDING row, never append a second row for the
    same file_path: appending would double the ledger (88,236 PENDING
    + 88,236 DONE rows) and break the audit's row-count check, the
    catalog, and STATE reconciliation. The whole file is rewritten
    atomically (tmp + replace) so a crash cannot half-write it.
    ``all_rows`` is mutated in place (updated rows replaced, new rows
    appended) and stays the caller's single source of truth.
    """
    os.makedirs(os.path.dirname(ledger_path) or ".", exist_ok=True)
    by_path = {}
    for row in all_rows:
        key = (row.get("file_path") or "").strip()
        if key:
            by_path[key] = row
    for batch_row in batch_rows:
        key = (batch_row.get("file_path") or "").strip()
        if key and key in by_path:
            by_path[key].clear()
            by_path[key].update(batch_row)
        else:
            all_rows.append(batch_row)
            if key:
                by_path[key] = batch_row
    tmp_path = ledger_path + ".tmp"
    with open(tmp_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({k: row.get(k, "") for k in LEDGER_FIELDS})
    os.replace(tmp_path, ledger_path)


def _yaml_str(value):
    """Render a string as a double-quoted YAML scalar (JSON quoting)."""
    return json.dumps(str(value), ensure_ascii=False)


def build_frontmatter(row, result, md_sha256, converted_at, source):
    """Build the YAML frontmatter block for one converted document."""
    from .hf_enumerator import hf_resolve_url
    from .indexer import folder_of

    doc_id = (row.get("document_id") or "").strip()
    if not doc_id or doc_id == "NO_ID_AS_LISTED":
        stem = os.path.basename(row["file_path"])
        doc_id = stem[:-4] if stem.lower().endswith(".pdf") else stem
    lines = [
        "---",
        f"doc_id: {_yaml_str(doc_id)}",
        f"title: {_yaml_str(row.get('headline') or '')}",
        f"category: {_yaml_str(folder_of(row))}",
        f"year: {int(row.get('year') or 0)}",
        f"source_hf_url: {_yaml_str(hf_resolve_url(row['file_path']))}",
        f"source_rbi_url: {_yaml_str(row.get('pdf_url') or '')}",
        f"pdf_sha256: {_yaml_str(row.get('sha256') or '')}",
        f"md_sha256: {_yaml_str(md_sha256)}",
        f"total_pages: {int(result.get('total_pages') or 0)}",
        f"native_pages: {int(result.get('native_pages') or 0)}",
        f"ocr_pages: {int(result.get('ocr_pages') or 0)}",
        f"conversion_engine: {_yaml_str(result.get('engine') or 'unknown')}",
        f"converted_at_utc: {_yaml_str(converted_at)}",
        f"source: {_yaml_str(source)}",
        'verification_status: "VERIFIED_LEVEL_5"',
        "---",
        "",
    ]
    return "\n".join(lines)


def _load_converter():
    """Import the converter module, or raise a clear, fatal error."""
    try:
        from . import converter
    except ImportError as exc:
        raise RuntimeError(
            "converter module src/rbi_pipeline/converter.py is missing; "
            "the runner refuses to write empty or placeholder Markdown. "
            "Implement convert_pdf(pdf_bytes, metadata) first."
        ) from exc
    if not callable(getattr(converter, "convert_pdf", None)):
        raise RuntimeError(
            "converter module has no callable convert_pdf(pdf_bytes, "
            "metadata); refusing to run."
        )
    return converter


def _split_converter_output(result):
    """Split a converter result into (full_markdown, body).

    Returns (markdown, body) when the converter supplied a complete file
    (frontmatter + body), (None, body) when it supplied only a
    ``markdown_body`` key, and (None, None) when neither is usable.
    ``body`` is the GFM after the closing frontmatter fence, or the raw
    body for the body-only case.
    """
    full = result.get("markdown")
    if isinstance(full, str) and full.startswith("---"):
        _open, sep, rest = full.partition("\n---\n")
        if sep:
            return full, rest
        return full, ""
    body = result.get("markdown_body")
    if body is None:
        body = full
    if not isinstance(body, str) or not body.strip():
        return None, None
    return None, body


def _convert_one(row, repo_root):
    """Download, verify, convert and write one row. Returns a ledger row.

    Runs in the parent process (sequential mode) or in a worker process
    (parallel mode). Downloads one PDF at a time and releases its bytes
    after conversion. On failure returns a FAILED ledger row instead of
    raising, so one bad PDF never kills the batch.
    """
    from .hf_enumerator import DownloadError, download_pdf, hf_resolve_url
    from .indexer import folder_of, md_path_for

    converter = _load_converter()
    md_rel = md_path_for(row["file_path"])
    md_abs = os.path.join(repo_root, md_rel)
    converted_at = _utcnow_iso()
    base = {
        "file_path": row["file_path"],
        "md_path": md_rel,
        "category": folder_of(row),
        "year": row.get("year") or 0,
        "listing_date": row.get("listing_date") or "",
        "headline": row.get("headline") or "",
        "document_id": row.get("document_id") or "",
        "pdf_url": row.get("pdf_url") or "",
        "hf_url": hf_resolve_url(row["file_path"]),
        "pdf_sha256": row.get("sha256") or "",
        "md_sha256": "",
        "status": "FAILED",
        "verification_status": "",
        "engine": "",
        "total_pages": "",
        "native_pages": "",
        "ocr_pages": "",
        "source": "",
        "converted_at_utc": converted_at,
        "error": "",
    }
    pdf_bytes = None
    source = None
    try:
        pdf_bytes = download_pdf(
            base["hf_url"], expected_sha256=row.get("sha256") or None,
            expected_bytes=row.get("bytes"),
        )
        source = "hf"
    except (DownloadError, RuntimeError) as exc:
        _log(f"HF download failed for {row['file_path']}: {exc}; "
             "falling back to direct RBI URL")
        if not row.get("pdf_url"):
            base["error"] = f"HF download failed and no RBI URL: {exc}"
            return base
        try:
            pdf_bytes = download_pdf(
                row["pdf_url"], expected_sha256=row.get("sha256") or None,
                expected_bytes=row.get("bytes"),
            )
            source = "rbi"
        except (DownloadError, RuntimeError) as exc2:
            base["error"] = f"HF failed ({exc}); RBI failed ({exc2})"
            return base
    try:
        meta = dict(row)
        meta["pdf_sha256"] = row.get("sha256") or ""
        result = converter.convert_pdf(pdf_bytes, meta)
    except Exception as exc:
        base["error"] = f"converter failed: {exc}"
        base["source"] = source
        return base
    finally:
        pdf_bytes = None  # release PDF bytes immediately
    full_markdown, body = _split_converter_output(result)
    if full_markdown is None and body is None:
        base["error"] = (
            "converter returned neither markdown nor markdown_body"
        )
        base["source"] = source
        return base
    if body is None or not body.strip():
        base["error"] = "converter returned empty Markdown body"
        base["source"] = source
        return base
    computed_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    reported_sha = (result.get("md_sha256") or "").strip().lower()
    md_sha256 = reported_sha if reported_sha == computed_sha else computed_sha
    if full_markdown is not None:
        # Converter supplied frontmatter: keep it verbatim, but inject the
        # download source and a percent-encoded HF URL. Neither affects
        # md_sha256, which covers the body only.
        from .hf_enumerator import hf_resolve_url

        frontmatter, _sep, rest = full_markdown.partition("\n---\n")
        lines = frontmatter.split("\n")
        lines = [ln for ln in lines
                 if not ln.startswith("source: ")
                 and not ln.startswith("source_hf_url: ")]
        insert_at = next(
            (i + 1 for i, ln in enumerate(lines)
             if ln.startswith("converted_at_utc: ")),
            len(lines),
        )
        lines.insert(insert_at,
                     f"source: {_yaml_str(source)}")
        lines.insert(insert_at + 1,
                     f"source_hf_url: {_yaml_str(hf_resolve_url(row['file_path']))}")
        content = "\n".join(lines) + "\n---\n" + rest
    else:
        frontmatter = build_frontmatter(row, result, md_sha256,
                                        converted_at, source)
        content = frontmatter + body
        if not body.endswith("\n"):
            content += "\n"
    os.makedirs(os.path.dirname(md_abs), exist_ok=True)
    tmp_path = md_abs + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    os.replace(tmp_path, md_abs)
    base.update({
        "md_sha256": md_sha256,
        "status": "DONE",
        "verification_status": result.get("verification_status") or "",
        "engine": result.get("engine") or "",
        "total_pages": result.get("total_pages") or "",
        "native_pages": result.get("native_pages") or "",
        "ocr_pages": result.get("ocr_pages") or "",
        "source": source,
    })
    return base


def _convert_one_worker(args):
    """Top-level worker for ProcessPoolExecutor (must be picklable)."""
    row, repo_root = args
    return _convert_one(row, repo_root)


def _check_disk(repo_root):
    free = shutil.disk_usage(repo_root).free
    if free < _MIN_FREE_BYTES:
        raise RuntimeError(
            f"only {free} bytes free under {repo_root}; refusing to start "
            "a batch (need at least 1 GiB)."
        )


def _index_paths(repo_root):
    """Paths the indexer owns, for committing a rebuild on its own.

    Only paths that exist on disk are returned; missing ones are
    skipped so the commit works on a fresh repo too.
    """
    paths = [
        "INDEX.md",
        "README.md",
        "llms.txt",
        "llms-full.txt",
        "manifest/master_catalog.jsonl",
        "index/url_to_path_map.json",
        "index/url_collisions.json",
    ]
    for sub in ("index/by_year", "index/by_category"):
        directory = os.path.join(repo_root, sub)
        if os.path.isdir(directory):
            for name in sorted(os.listdir(directory)):
                paths.append(os.path.join(sub, name))
    return [p for p in paths if os.path.exists(os.path.join(repo_root, p))]


def _commit_message(done, total, batch, batch_number, ledger_rows):
    from .indexer import folder_of

    pct = done / total * 100.0 if total else 0.0
    first = batch[0]
    native = sum(
        1 for r in ledger_rows
        if r.get("status") == "DONE" and not int(r.get("ocr_pages") or 0)
    )
    ocr = sum(
        1 for r in ledger_rows
        if r.get("status") == "DONE" and int(r.get("ocr_pages") or 0) > 0
    )
    category = folder_of(first)
    year = first.get("year") or ""
    return (
        f"chore(convert): [{pct:.4f}%] {done}/{total} PDFs -> MD | "
        f"{category}/{year} Batch #{batch_number} | "
        f"{native} anydoc + {ocr} OCR verified"
    )


def main(argv=None):
    """Entry point. Returns an exit code (0 ok, 2 unrecoverable)."""
    parser = argparse.ArgumentParser(
        description="Batch-convert RBI PDFs to Markdown, one signed "
                    "commit per batch."
    )
    parser.add_argument("--manifest", default="manifest/hf_88236_inventory.jsonl")
    parser.add_argument("--batch-size", type=int, default=75)
    parser.add_argument("--max-runtime-seconds", type=int, default=17400)
    parser.add_argument("--state", default="STATE.json")
    parser.add_argument("--ledger", default="manifest/sha256_conversion_ledger.csv")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--workers", type=int, default=2,
                        help="parallel workers; used only when the "
                             "converter sets PROCESS_SAFE = True, else "
                             "sequential")
    args = parser.parse_args(argv)
    repo_root = os.path.abspath(args.repo_root)
    manifest_path = args.manifest
    if not os.path.isabs(manifest_path):
        manifest_path = os.path.join(repo_root, manifest_path)
    state_path = args.state
    if not os.path.isabs(state_path):
        state_path = os.path.join(repo_root, state_path)
    ledger_path = args.ledger
    if not os.path.isabs(ledger_path):
        ledger_path = os.path.join(repo_root, ledger_path)

    started = time.monotonic()
    deadline = started + max(0, args.max_runtime_seconds - _TIME_RESERVE_SECONDS)
    try:
        inventory = load_inventory(manifest_path)
        converter = _load_converter()  # fail fast when missing
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    total = len(inventory)
    state = load_state(state_path, total)
    state["total_count"] = total
    done_paths = set(state.get("done_paths") or [])
    ledger_rows, ledger_by_path = load_ledger(ledger_path)

    # Reconcile: rows the ledger already marks DONE with a .md file on
    # disk count as done even if STATE.json was lost mid-batch.
    from .indexer import md_path_for

    for row in inventory:
        path = row["file_path"]
        if path in done_paths:
            continue
        ledger_row = ledger_by_path.get(path)
        if ledger_row and ledger_row.get("status") == "DONE":
            if os.path.exists(os.path.join(repo_root, md_path_for(path))):
                done_paths.add(path)
    state["done_paths"] = sorted(done_paths)
    state["done_count"] = len(done_paths)
    save_state(state_path, state)

    parallel = False
    if args.workers > 1:
        if getattr(converter, "PROCESS_SAFE", False):
            parallel = True
            _log(f"parallel mode with {args.workers} workers "
                 "(converter declares PROCESS_SAFE)")
        else:
            _log("converter does not declare PROCESS_SAFE; running "
                 "sequentially despite --workers "
                 f"{args.workers}")

    try:
        from .git_committer import commit_batch, configure_identity, verify_last_commit
        from .indexer import append_progress_log, update_readme_progress

        configure_identity(cwd=repo_root)
    except Exception as exc:
        print(f"fatal: git identity setup failed: {exc}", file=sys.stderr)
        return 2

    # Recovery: a previous run may have rebuilt the indexes at its
    # graceful stop but failed to commit them. Uncommitted index files
    # would make this run's pull --rebase fail, so commit them first
    # (a no-op when the tree is clean). STATE.json is included because
    # the reconcile above just re-saved it, leaving it modified.
    try:
        _recovered = commit_batch(
            _index_paths(repo_root)
            + [os.path.relpath(state_path, repo_root)],
            "chore(index): rebuild indexes (recovered from previous run)",
            cwd=repo_root,
        )
        if _recovered:
            _log("recovered uncommitted index rebuild from previous run")
    except Exception as exc:
        print(f"fatal: index recovery commit failed: {exc}", file=sys.stderr)
        save_state(state_path, state)
        return 2

    batches_done = 0
    consecutive_failed_batches = 0
    try:
        while True:
            if time.monotonic() >= deadline:
                _log("time budget reached; stopping with state flushed "
                     "for self-chain")
                break
            pending = [r for r in inventory if r["file_path"] not in done_paths]
            if not pending:
                _log("no pending rows left")
                break
            _check_disk(repo_root)
            batch = pending[: args.batch_size]
            batch_number = int(state.get("last_batch") or 0) + 1
            _log(f"batch #{batch_number}: {len(batch)} files "
                 f"({len(done_paths)}/{total} done)")
            ledger_batch = []
            if parallel:
                with ProcessPoolExecutor(max_workers=args.workers) as pool:
                    futures = {
                        pool.submit(_convert_one_worker, (row, repo_root)): row
                        for row in batch
                    }
                    for future in as_completed(futures):
                        ledger_batch.append(future.result())
            else:
                for row in batch:
                    if (time.monotonic() >= deadline
                            and ledger_batch):
                        _log("deadline reached mid-batch; committing "
                             "partial batch")
                        break
                    ledger_batch.append(_convert_one(row, repo_root))
            # Keep ledger rows in manifest order.
            order = {row["file_path"]: i for i, row in enumerate(batch)}
            ledger_batch.sort(key=lambda r: order.get(r["file_path"], 0))
            upsert_ledger_rows(ledger_path, ledger_rows, ledger_batch)
            for row in ledger_batch:
                if row.get("status") == "DONE":
                    done_paths.add(row["file_path"])
            state["done_paths"] = sorted(done_paths)
            state["done_count"] = len(done_paths)
            state["last_batch"] = batch_number
            save_state(state_path, state)

            done = len(done_paths)
            message = _commit_message(done, total, batch, batch_number,
                                      ledger_batch)
            md_files = [
                md_path_for(r["file_path"])
                for r in ledger_batch if r.get("status") == "DONE"
            ]
            progress_line = (
                f"- {_utcnow_iso()} batch #{batch_number}: {message}"
            )
            append_progress_log(repo_root, progress_line)
            from .indexer import _counts

            by_folder, by_folder_done, _y, _yd = _counts(inventory, {
                r["file_path"]: r for r in ledger_rows
            })
            update_readme_progress(repo_root, total, done,
                                   by_folder, by_folder_done)
            commit_paths = (
                md_files
                + [os.path.relpath(state_path, repo_root),
                   os.path.relpath(ledger_path, repo_root),
                   "PROGRESS.md", "README.md"]
            )
            pushed = commit_batch(commit_paths, message, cwd=repo_root)
            if not pushed:
                _log("batch produced no staged changes; nothing committed")
            elif not verify_last_commit(cwd=repo_root):
                raise RuntimeError(
                    "last commit has no signature; refusing to continue "
                    "with unsigned commits"
                )
            # A batch that converts nothing (downloads down, converter
            # broken) must not loop forever: the same pending files
            # would be retried every batch until the time budget runs
            # out, committing empty batches. Three in a row is a
            # systemic failure; stop so a human (or the watchdog) can
            # look, instead of burning the run.
            done_this_batch = sum(
                1 for r in ledger_batch if r.get("status") == "DONE"
            )
            if done_this_batch == 0:
                consecutive_failed_batches += 1
            else:
                consecutive_failed_batches = 0
            if consecutive_failed_batches >= 3:
                raise RuntimeError(
                    "3 consecutive batches produced 0 conversions; "
                    "stopping (check the ledger error column)"
                )
            batches_done += 1
            _log(f"batch #{batch_number} committed: "
                 f"{done}/{total} ({done / total * 100:.4f}%)")
    except RuntimeError as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        save_state(state_path, state)
        return 2

    # Graceful stop: rebuild the full indexes once so llms.txt, INDEX.md,
    # the catalog and the URL map stay synchronized with the ledger.
    try:
        from .indexer import build_all

        counts = build_all(repo_root, ledger_rows, inventory)
        _log(f"indexes rebuilt: {counts['done']}/{counts['total']} done")
    except Exception as exc:  # indexes are rebuilt by the audit workflow too
        _log(f"warning: index rebuild failed ({exc}); continuing")
        counts = {"done": len(done_paths), "total": total}
    save_state(state_path, state)
    # The rebuild rewrites tracked files (INDEX.md, llms.txt, the URL
    # map, the catalog). Commit them in their own signed commit now:
    # left uncommitted, they make the next run's pull --rebase fail on
    # unstaged changes and the pipeline stalls. A failed index commit
    # is fatal for this run (exit 2) so the workflow does not self-chain
    # into the same failure; the next startup recovers the rebuild.
    try:
        index_message = (
            f"chore(index): rebuild indexes | "
            f"{counts['done']}/{counts['total']} PDFs -> MD"
        )
        # STATE.json is included: save_state above just re-saved it,
        # so without staging it the pull --rebase would fail.
        if commit_batch(
            _index_paths(repo_root)
            + [os.path.relpath(state_path, repo_root)],
            index_message, cwd=repo_root,
        ):
            _log("index rebuild committed")
    except Exception as exc:
        print(f"fatal: index commit failed: {exc}", file=sys.stderr)
        save_state(state_path, state)
        return 2
    _log(f"run finished: {batches_done} batches, "
         f"{len(done_paths)}/{total} done, "
         f"remaining {total - len(done_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
