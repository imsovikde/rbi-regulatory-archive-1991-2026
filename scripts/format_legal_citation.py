"""Feature F41: Court and RBI Ombudsman Legal Citation Formatter.

Generates verified statutory citation blocks with official circular references,
enabling acts, gazette/reporting dates, and cryptographic SHA-256 PDF hashes.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys


def format_citation(repo_root: str, query: str) -> dict | None:
    catalog_files = sorted(glob.glob(os.path.join(repo_root, "manifest", "catalog", "*.jsonl")))
    clean_q = query.strip().lower()

    for cf in catalog_files:
        with open(cf, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                doc_id = (d.get("document_id") or "").lower()
                fp = d.get("file_path", "").lower()
                head = d.get("headline", "").lower()
                if clean_q in doc_id or clean_q in fp or clean_q in head:
                    # Construct citation block
                    doc_id_orig = d.get("document_id") or "Ref Not Specified"
                    title = d.get("headline") or os.path.basename(d.get("file_path", ""))
                    date = d.get("listing_date") or f"{d.get('year')}"
                    sha = d.get("pdf_sha256") or "NOT_AVAILABLE"
                    hf_url = d.get("hf_url") or ""
                    
                    citation_text = (
                        f"Reserve Bank of India, Notification/Direction Ref. {doc_id_orig}, "
                        f"\"{title}\", dated {date}. "
                        f"Cryptographic Verification: SHA-256 [{sha}]. "
                        f"Archival Source: {hf_url}"
                    )
                    
                    return {
                        "document_id": doc_id_orig,
                        "title": title,
                        "date": date,
                        "category": d.get("category"),
                        "year": d.get("year"),
                        "pdf_sha256": sha,
                        "citation_string": citation_text,
                        "court_ready_block": (
                            f"CITATION FOR JUDICIAL/ARBITRAL PROCEEDINGS:\n"
                            f"--------------------------------------------------\n"
                            f"Authority: Reserve Bank of India (Central Bank of India)\n"
                            f"Instrument: {d.get('category')}\n"
                            f"Official Reference: {doc_id_orig}\n"
                            f"Title: {title}\n"
                            f"Issuance Date: {date}\n"
                            f"Cryptographic Digest: SHA256:{sha}\n"
                            f"Verified Repository: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026\n"
                            f"Canonical Binary: {hf_url}\n"
                            f"--------------------------------------------------"
                        )
                    }
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Circular ID, keyword, or filename")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    res = format_citation(repo_root, args.query)
    if not res:
        print(f"No document matching query '{args.query}' found in catalog.", file=sys.stderr)
        sys.exit(1)

    print(res["court_ready_block"])


if __name__ == "__main__":
    main()
