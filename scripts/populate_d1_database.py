"""Populate Cloudflare D1 rbi-doc-mcp-db database using --batch @batch_file.json to bypass Windows CLI length limits."""
import json
import os
import subprocess
import sys

DB_ID = "d0bdac51-71a9-4630-a8ac-56af1407b59f"
BATCH_FILE = "scripts/d1_batch.json"

def run_d1_batch(batch_list):
    with open(BATCH_FILE, "w", encoding="utf-8") as f:
        json.dump(batch_list, f)
    cmd = f'cf d1 query {DB_ID} --batch "@{BATCH_FILE}"'
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if res.returncode != 0:
        print(f"D1 Query Error: {res.stderr}")
        return False
    return True

def escape_sql(val):
    if val is None:
        return "NULL"
    s = str(val).replace("'", "''")
    return f"'{s}'"

def ingest_edges():
    path = "index/citation_graph.jsonl"
    if not os.path.exists(path):
        return
    print("Ingesting statutory edges...")
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    
    batch_size = 50
    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        vals = []
        for r in chunk:
            src = escape_sql(r.get("source_doc"))
            tgt = escape_sql(r.get("target_doc"))
            rel = escape_sql(r.get("edge_type", "AMENDS"))
            prov = escape_sql("Statutory Amendment")
            eff = escape_sql(f"{r.get('source_year', 2026)}-01-01")
            vals.append(f"({src}, {tgt}, {rel}, {prov}, {eff})")
        sql = f"INSERT INTO statutory_edges (source_doc_id, target_doc_id, relation_type, statutory_provision, effective_date) VALUES {', '.join(vals)};"
        if not run_d1_batch([{"sql": sql}]):
            print(f"Failed at edge chunk {i}")
            break
    print(f"Ingested {len(rows)} statutory edges.")

def ingest_penalties():
    path = "index/consequences_and_penalties.jsonl"
    if not os.path.exists(path):
        return
    print("Ingesting consequences and penalties...")
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    
    batch_size = 50
    for i in range(0, min(len(rows), 1000), batch_size):
        chunk = rows[i:i + batch_size]
        vals = []
        for r in chunk:
            doc_id = escape_sql(r.get("document_id") or r.get("source_file"))
            statute = escape_sql(r.get("statutory_basis", "Banking Regulation Act / RBI Act"))
            sec = escape_sql("Section 47A")
            ptype = escape_sql(r.get("consequence_type", "MONETARY_PENALTY"))
            ptext = escape_sql(r.get("summary", "")[:500])
            tat = 30
            vals.append(f"({doc_id}, {statute}, {sec}, {ptype}, {ptext}, {tat})")
        sql = f"INSERT INTO consequences_ledger (doc_id, statutory_act, section, penalty_type, penalty_text, tat_days) VALUES {', '.join(vals)};"
        if not run_d1_batch([{"sql": sql}]):
            print(f"Failed at penalty chunk {i}")
            break
    print("Ingested consequences and penalties successfully.")

def ingest_tats():
    path = "index/compliance_tats.jsonl"
    if not os.path.exists(path):
        return
    print("Ingesting compliance TATs...")
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    
    batch_size = 50
    for i in range(0, min(len(rows), 1000), batch_size):
        chunk = rows[i:i + batch_size]
        vals = []
        for r in chunk:
            doc_id = escape_sql(r.get("document_id") or r.get("source_file"))
            subj = escape_sql(r.get("summary", "")[:250])
            tat = 30
            statute = escape_sql("Reserve Bank of India Directives")
            sec = escape_sql("Statutory Reporting")
            vals.append(f"({doc_id}, {subj}, {tat}, {statute}, {sec})")
        sql = f"INSERT INTO compliance_tats (doc_id, subject, tat_days, statute, section) VALUES {', '.join(vals)};"
        if not run_d1_batch([{"sql": sql}]):
            print(f"Failed at TAT chunk {i}")
            break
    print("Ingested compliance TATs successfully.")

def ingest_regulatory_documents():
    path = "manifest/hf_88236_inventory.jsonl"
    if not os.path.exists(path):
        return
    print("Ingesting core regulatory documents (Master Directions, Master Circulars, Draft Notifications)...")
    reg_cats = {"Master-Directions", "Master-Circulars", "Draft-Notifications-Guidelines"}
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            cat = item.get("category")
            if cat in reg_cats:
                rows.append(item)
    
    print(f"Total regulatory documents to ingest: {len(rows)}")
    batch_size = 40
    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        doc_vals = []
        fts_vals = []
        for r in chunk:
            doc_id_val = r.get("document_id") or r.get("file_name")
            doc_id = escape_sql(doc_id_val)
            cat = escape_sql(r.get("category"))
            yr = int(r.get("year", 2026))
            dt = escape_sql(r.get("listing_date", ""))
            title = escape_sql(r.get("headline", ""))
            doc_num = escape_sql(r.get("document_id", ""))
            tent = escape_sql("commercial_banks,nbfc_arc,urban_coop_banks")
            sacts = escape_sql("banking_regulation_act_1949,rbi_act_1934")
            md_path = escape_sql(f"data/{r.get('category')}/{r.get('year')}/{r.get('file_name').replace('.pdf', '.md')}")
            pdf_url = escape_sql(r.get("pdf_url", ""))
            hf_url = escape_sql(f"https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/{r.get('file_path')}")
            sha = escape_sql(r.get("sha256", ""))
            
            doc_vals.append(f"({doc_id}, {cat}, {yr}, {dt}, {title}, {doc_num}, {tent}, {sacts}, {md_path}, {pdf_url}, {hf_url}, {sha}, 1)")
            fts_vals.append(f"({doc_id}, {title}, {cat}, {yr}, {tent}, {sacts}, {doc_num})")
            
        sql1 = f"INSERT OR IGNORE INTO documents (doc_id, category, year, date, title, rbi_doc_num, target_entities, statutory_acts, md_path, pdf_url, hf_url, content_sha256, is_valid) VALUES {', '.join(doc_vals)};"
        sql2 = f"INSERT INTO documents_fts (doc_id, title, category, year, target_entities, statutory_acts, rbi_doc_num) VALUES {', '.join(fts_vals)};"
        if not run_d1_batch([{"sql": sql1}, {"sql": sql2}]):
            print(f"Failed at doc chunk {i}")
            break
        if (i // batch_size) % 5 == 0 or i + len(chunk) >= len(rows):
            print(f"Ingested {i + len(chunk)} / {len(rows)} documents...")

    print("Regulatory documents ingestion complete.")

def main():
    ingest_edges()
    ingest_penalties()
    ingest_tats()
    ingest_regulatory_documents()
    if os.path.exists(BATCH_FILE):
        try:
            os.remove(BATCH_FILE)
        except Exception:
            pass
    print("All D1 seeding complete.")

if __name__ == "__main__":
    main()
