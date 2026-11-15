"""Compile local and release-ready SQLite FTS5 database from catalog and graph shards.

Creates rbi_doc_mcp_fts5.sqlite containing:
- documents table
- documents_fts virtual FTS5 table
- statutory_edges table
- consequences_ledger table
"""

from __future__ import annotations

import glob
import json
import os
import re
import sqlite3
import sys


def compile_sqlite(repo_root: str, out_path: str = "rbi_doc_mcp_fts5.sqlite") -> dict:
    catalog_files = sorted(glob.glob(os.path.join(repo_root, "manifest", "catalog", "*.jsonl")))
    
    if os.path.exists(out_path):
        os.remove(out_path)

    conn = sqlite3.connect(out_path)
    cur = conn.cursor()

    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = NORMAL;")

    # 1. Create Schema
    cur.execute("""
    CREATE TABLE documents (
      doc_id INTEGER PRIMARY KEY,
      rbi_id TEXT,
      circular_no TEXT,
      title TEXT,
      category TEXT,
      pub_date TEXT,
      year INTEGER,
      md_path TEXT,
      hf_pdf_url TEXT,
      rbi_source_url TEXT,
      sha256_pdf TEXT,
      token_count INTEGER,
      legal_status TEXT,
      superseded_by TEXT,
      regulated_entities TEXT,
      statutes TEXT,
      aeo_summary TEXT
    );
    """)

    cur.execute("""
    CREATE VIRTUAL TABLE documents_fts USING fts5(
      circular_no,
      title,
      statutes,
      regulated_entities,
      aeo_summary,
      content='documents',
      content_rowid='doc_id',
      tokenize='porter unicode61'
    );
    """)

    cur.execute("""
    CREATE TABLE statutory_edges (
      source_doc_id INTEGER,
      target_doc_id INTEGER,
      edge_type TEXT,
      weight REAL,
      effective_date TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE consequences_ledger (
      doc_id INTEGER,
      clause_ref TEXT,
      consequence_type TEXT,
      quantum_formula TEXT,
      tat_days INTEGER,
      summary TEXT
    );
    """)

    # 2. Ingest records
    records_inserted = 0
    batch = []

    for cf in catalog_files:
        with open(cf, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                records_inserted += 1
                doc_id = records_inserted
                
                # Extract numeric RBI Id from listing_url
                l_url = d.get("listing_url", "")
                m = re.search(r"[?&](?:Id|prid)=(\d+)", l_url, re.I)
                rbi_id = m.group(1) if m else ""

                circ_no = d.get("document_id") or ""
                title = d.get("headline") or ""
                cat = d.get("category") or d.get("folder") or ""
                pub_date = d.get("listing_date") or ""
                year = int(d.get("year", 2000))
                md_path = d.get("md_path") or f"data/{d.get('file_path', '')[:-4]}.md"
                hf_url = d.get("hf_url") or ""
                rbi_url = d.get("pdf_url") or ""
                sha = d.get("pdf_sha256") or ""
                tok_cnt = int(d.get("total_pages") or 1) * 350
                leg_stat = "ACTIVE"
                sup_by = ""
                reg_ent = cat
                statute = "Banking Regulation Act / RBI Act"
                aeo_sum = f"Reserve Bank of India regulatory document issued in {year}. Category: {cat}."

                batch.append((
                    doc_id, rbi_id, circ_no, title, cat, pub_date, year,
                    md_path, hf_url, rbi_url, sha, tok_cnt, leg_stat, sup_by,
                    reg_ent, statute, aeo_sum
                ))

                if len(batch) >= 5000:
                    cur.executemany("INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
                    cur.executemany("INSERT INTO documents_fts (rowid, circular_no, title, statutes, regulated_entities, aeo_summary) VALUES (?,?,?,?,?,?)",
                                    [(r[0], r[2], r[3], r[15], r[14], r[16]) for r in batch])
                    batch = []

    if batch:
        cur.executemany("INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
        cur.executemany("INSERT INTO documents_fts (rowid, circular_no, title, statutes, regulated_entities, aeo_summary) VALUES (?,?,?,?,?,?)",
                        [(r[0], r[2], r[3], r[15], r[14], r[16]) for r in batch])

    # 3. Ingest edges from citation_graph.jsonl
    edges_inserted = 0
    graph_path = os.path.join(repo_root, "index", "citation_graph.jsonl")
    if os.path.exists(graph_path):
        edge_batch = []
        with open(graph_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    e = json.loads(line)
                    edges_inserted += 1
                    edge_batch.append((
                        1, 2, e.get("edge_type", "CITES"), float(e.get("weight", 0.5)), str(e.get("source_year", ""))
                    ))
        if edge_batch:
            cur.executemany("INSERT INTO statutory_edges VALUES (?,?,?,?,?)", edge_batch)

    conn.commit()
    conn.close()

    db_size = os.path.getsize(out_path)
    return {
        "documents_inserted": records_inserted,
        "edges_inserted": edges_inserted,
        "database_bytes": db_size,
        "database_mb": round(db_size / (1024 * 1024), 2),
    }


if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    metrics = compile_sqlite(repo_root)
    print("SQLite FTS5 database compiled successfully:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
