"""Upload binary index artifacts to Cloudflare R2 bucket rbi-doc-mcp-corpus using cf CLI."""
import subprocess
import sys
import os

ARTIFACTS = [
    ("index/mphf_seeds.bin", "index/mphf_seeds.bin"),
    ("index/mphf_strings.bin", "index/mphf_strings.bin"),
    ("index/rbi_corpus.zdict", "index/rbi_corpus.zdict"),
    ("index/jacobian_neumann_csr.bin", "index/jacobian_neumann_csr.bin"),
    ("manifest/state_ef.bin", "manifest/state_ef.bin"),
    ("rbi_doc_mcp_fts5.sqlite.zst", "rbi_doc_mcp_fts5.sqlite.zst"),
    ("index/citation_graph.jsonl", "index/citation_graph.jsonl"),
    ("index/consequences_and_penalties.jsonl", "index/consequences_and_penalties.jsonl"),
    ("index/compliance_tats.jsonl", "index/compliance_tats.jsonl"),
    ("index/glossary.json", "index/glossary.json"),
    ("index/seo_schema_dataset.json", "index/seo_schema_dataset.json"),
    ("index/rbi_id_map/rbi_numeric_id_map.json", "index/rbi_id_map/rbi_numeric_id_map.json"),
]

def main():
    print("Uploading binary and JSON artifacts to R2 rbi-doc-mcp-corpus...")
    for key, path in ARTIFACTS:
        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue
        size_kb = os.path.getsize(path) / 1024
        print(f"Uploading {key} ({size_kb:.1f} KB)...")
        cmd = [
            "cf", "r2", "objects", "put", key,
            "--bucket-name", "rbi-doc-mcp-corpus",
            "--file", path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if res.returncode != 0:
            print(f"Failed to upload {key}: {res.stderr}")
            sys.exit(1)
        print(f"Uploaded {key} successfully.")
    print("All artifacts uploaded to R2 successfully.")

if __name__ == "__main__":
    main()
