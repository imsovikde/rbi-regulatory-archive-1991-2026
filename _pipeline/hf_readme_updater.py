#!/usr/bin/env python3
"""Hugging Face dataset card README.md synchronizer.

Generates and uploads the canonical dataset card to
https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026
with live document counts, category breakdowns, and GitHub Markdown links.
"""

from __future__ import annotations

import argparse
import os
import sys

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SCRIPTS_DIR)

from src.rbi_pipeline.dynamic_meta import get_archive_metrics, HF_FOLDERS

DATASET_REPO = "imsovikde/rbi-regulatory-archive-1991-2026"


def build_hf_dataset_card_text(metrics: dict) -> str:
    total = metrics["total_pdfs"]
    done = metrics["total_done"]
    year_min = metrics["year_min"]
    year_max = metrics["year_max"]
    by_folder = metrics["by_folder"]
    by_folder_done = metrics["by_folder_done"]

    lines = [
        "---",
        "annotations_creators:",
        "- no-annotation",
        "language:",
        "- en",
        "- hi",
        "language_creators:",
        "- original-data",
        "license:",
        "- cc0-1.0",
        "multilinguality:",
        "- multilingual",
        "size_categories:",
        "- 10K<n<100K",
        "source_datasets:",
        "- original",
        "tags:",
        "- legal",
        "- rbi",
        "- finance",
        "- banking",
        "- regulatory",
        "- india",
        "- pdf",
        "task_categories:",
        "- text-retrieval",
        "- question-answering",
        "task_ids:",
        "- document-retrieval",
        f"pretty_name: Reserve Bank of India Regulatory Archive 1991-{year_max}",
        "---",
        "",
        f"# Reserve Bank of India Regulatory Archive (1991-{year_max})",
        "",
        f"Untouched source PDF binaries for every Reserve Bank of India regulatory document from 1991 through {year_max}.",
        "",
        "## Converted Markdown Archive",
        "",
        "The converted GitHub-Flavored Markdown archive, statutory graph router, and llms.txt index live at:",
        "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026",
        "",
        "## Live Document Census",
        "",
        f"- **Total PDF Documents:** {total:,}",
        f"- **Converted to Markdown:** {done:,}",
        f"- **Conversion Status:** {metrics['pct']:.4f}% complete",
        f"- **Temporal Span:** {year_min} through {year_max}",
        "",
        "| Category | Total PDFs | Converted to Markdown | Coverage |",
        "| --- | ---: | ---: | ---: |",
    ]

    for cat in HF_FOLDERS:
        tot = by_folder.get(cat, 0)
        c_done = by_folder_done.get(cat, 0)
        pct = (c_done / tot * 100.0) if tot else 100.0
        lines.append(f"| {cat} | {tot:,} | {c_done:,} | {pct:.4f}% |")

    lines.extend([
        "",
        "## File Organization",
        "",
        "PDFs are stored in category and year folders matching the GitHub Markdown repository:",
        "```text",
        "<Category>/<YYYY>/YYYY-MM-DD_<Category>_<Document-ID>_<Headline>.pdf",
        "```",
        "",
        "## Maintenance & Provenance",
        "",
        "Maintained by Souvik Dey (https://github.com/imsovikde).",
        "Weekly automated synchronization checks live Reserve Bank of India endpoints and updates both Hugging Face and GitHub.",
    ])

    return "\n".join(lines) + "\n"


def sync_hf_card(repo_root: str, token: str | None = None, dry_run: bool = False) -> bool:
    token = token or os.environ.get("HF_TOKEN")
    metrics = get_archive_metrics(repo_root)
    card_text = build_hf_dataset_card_text(metrics)

    if dry_run or not token:
        print(f"Hugging Face Card sync (dry-run={dry_run}, token_set={bool(token)}):")
        print(f"Generated card text for {metrics['total_pdfs']} PDFs (1991-{metrics['year_max']})")
        return True

    try:
        from huggingface_hub import HfApi
        api = HfApi(token=token)
        api.upload_file(
            path_or_fileobj=card_text.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message=f"chore: update dataset card counts | {metrics['total_done']}/{metrics['total_pdfs']} PDFs",
        )
        print(f"Hugging Face dataset card README.md uploaded successfully to {DATASET_REPO}.")
        return True
    except Exception as exc:
        print(f"warning: HfApi upload failed ({exc}). Continuing fallback mode.", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="build card text without uploading")
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ok = sync_hf_card(repo_root, dry_run=args.dry_run)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
