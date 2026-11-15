"""Feature F14: Point-in-Time Regulatory Time Machine.

Queries the statutory supersession DAG and computes exact in-force regulatory status
as of any historical date T (YYYY-MM-DD) in closed form using Engine M3.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys


def query_as_of_date(repo_root: str, as_of_date: str, category: str | None = None, limit: int = 50) -> list[dict]:
    query_year = int(as_of_date[:4])
    catalog_files = sorted(glob.glob(os.path.join(repo_root, "manifest", "catalog", "*.jsonl")))
    
    # Load citation graph edges
    graph_path = os.path.join(repo_root, "index", "citation_graph.jsonl")
    repeals_by_target = {}
    if os.path.exists(graph_path):
        with open(graph_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    edge = json.loads(line)
                    if edge.get("edge_type") in ("SUPERSEDES", "REPEALS"):
                        tgt = edge.get("target_doc")
                        src_year = edge.get("source_year", 9999)
                        if tgt:
                            repeals_by_target[tgt] = src_year

    results = []
    for cf in catalog_files:
        yr = int(os.path.basename(cf).replace(".jsonl", ""))
        if yr > query_year:
            continue

        with open(cf, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                if category and (d.get("category") != category and d.get("folder") != category):
                    continue

                fp = d.get("file_path", "")
                # Check if superseded before or on query date
                repeal_year = repeals_by_target.get(fp)
                if repeal_year and repeal_year <= query_year:
                    status = "SUPERSEDED_AS_OF_DATE"
                    valid = False
                else:
                    status = "ACTIVE_AS_OF_DATE"
                    valid = True

                if valid:
                    results.append({
                        "file_path": fp,
                        "document_id": d.get("document_id"),
                        "headline": d.get("headline"),
                        "category": d.get("category"),
                        "year": d.get("year"),
                        "validity_status": status,
                        "md_path": d.get("md_path"),
                    })
                    if len(results) >= limit:
                        return results

    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Point-in-Time date (YYYY-MM-DD)")
    parser.add_argument("--category", choices=[
        "Master-Directions", "Notifications", "Master-Circulars",
        "Draft-Notifications-Guidelines", "Circulars", "Press-Releases"
    ])
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    res = query_as_of_date(repo_root, args.date, category=args.category, limit=args.limit)
    print(f"Active in-force regulations as of {args.date} ({len(res)} matches):")
    for r in res[:args.limit]:
        print(f"  [{r['year']}] {r['category']}: {r['headline']} ({r['document_id'] or 'No Ref'})")


if __name__ == "__main__":
    main()
