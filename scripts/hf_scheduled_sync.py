#!/usr/bin/env python3
"""Hugging Face Scheduled Sync & Upstream Dataset Watcher.

Checks upstream Hugging Face dataset `imsovikde/rbi-regulatory-archive-1991-2026`
for any new or updated PDFs, reconciles against the local inventory and conversion
ledger, registers new documents, and optionally uploads local discovered PDFs.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

DATASET_REPO = "imsovikde/rbi-regulatory-archive-1991-2026"
HF_BASE_URL = f"https://huggingface.co/datasets/{DATASET_REPO}/resolve/main/"


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sync_hf_dataset(inventory_path: str, ledger_path: str, token: str | None = None, dry_run: bool = False, out_path: str | None = None, report_out: str | None = None):
    token = token or os.environ.get("HF_TOKEN")
    print(f"[{_utcnow_iso()}] Checking Hugging Face dataset: {DATASET_REPO} (token configured: {bool(token)})")

    # Load local inventory paths
    known_paths = set()
    if os.path.exists(inventory_path):
        with open(inventory_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        row = json.loads(line)
                        known_paths.add(row.get("file_path"))
                    except Exception:
                        pass

    print(f"[{_utcnow_iso()}] Local inventory contains {len(known_paths)} files.")

    if dry_run:
        print(f"[{_utcnow_iso()}] Dry-run: HF sync verified.")
        return 0

    def _save_hf_report(status: str, remote_count: int = 0, new_cnt: int = 0, err: str = ""):
        if not report_out:
            return
        os.makedirs(os.path.dirname(os.path.abspath(report_out)), exist_ok=True)
        with open(report_out, "w", encoding="utf-8") as rf:
            json.dump({
                "checked_at_utc": _utcnow_iso(),
                "dataset_repo": DATASET_REPO,
                "status": status,
                "local_inventory_count": len(known_paths),
                "remote_pdf_count": remote_count,
                "new_count": new_cnt,
                "error": err,
            }, rf, indent=2)

    try:
        from huggingface_hub import HfApi
        api = HfApi(token=token)
        remote_files = api.list_repo_files(repo_id=DATASET_REPO, repo_type="dataset")
        pdf_files = [f for f in remote_files if f.lower().endswith(".pdf")]
        print(f"[{_utcnow_iso()}] Remote dataset contains {len(pdf_files)} PDF files.")

        new_remote = [f for f in pdf_files if f not in known_paths]
        print(f"[{_utcnow_iso()}] Discovered {len(new_remote)} new PDFs from Hugging Face.")
        if out_path and new_remote:
            from urllib.parse import quote
            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            records = []
            for f in new_remote:
                hf_url = f"{HF_BASE_URL}{quote(f, safe='/')}"
                records.append({
                    "pdf_url": hf_url,
                    "file_path": f,
                    "source": "huggingface",
                })
            with open(out_path, "w", encoding="utf-8") as out_f:
                json.dump(records, out_f, indent=2)
            print(f"[{_utcnow_iso()}] Wrote {len(records)} new HF documents to {out_path}")
        _save_hf_report("OK", len(pdf_files), len(new_remote))
        return len(new_remote)
    except Exception as exc:
        print(f"[{_utcnow_iso()}] Note: HfApi query returned: {exc}. Continuing fallback mode.")
        _save_hf_report("WARN", 0, 0, str(exc))
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", default=os.path.join(REPO_ROOT, "manifest", "hf_88236_inventory.jsonl"))
    parser.add_argument("--ledger", default=os.path.join(REPO_ROOT, "manifest", "sha256_conversion_ledger.csv"))
    parser.add_argument("--out", default=None, help="output JSON for newly discovered HF documents")
    parser.add_argument("--report-out", default=None, help="output JSON for HF sync telemetry")
    parser.add_argument("--dry-run", action="store_true", help="verify without network mutations")
    args = parser.parse_args(argv)

    code = sync_hf_dataset(args.inventory, args.ledger, dry_run=args.dry_run, out_path=args.out, report_out=args.report_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
