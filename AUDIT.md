# Ralph-Loop 10-Gate Integrity Audit 2026-11-15 — 9/10 checks passed (FAIL)

<!-- RESULT passed=9 total=10 items_passed=353116 items_total=353117 verdict=FAIL -->

- [PASS] A: 1:1 file parity (valid frontmatter, body SHA matches): 88236/88236
- [PASS] B: compact STATE.json (<5KB, 100.0%, remaining=0): 1/1
- [FAIL] C: commit authored by Souvik Dey & verified GPG signature: 0/1
  - last commit GPG signature status is 'N', expected 'G' or 'U'
- [PASS] D: url_to_path_map & 256-shard coverage: 1/1
- [PASS] E: zero broken relative links & URL encoding: 176472/176472
- [PASS] F: non-empty Category column in yearly indexes: 88242/88242
- [PASS] G: per-directory INDEX.md coverage across all 161 folders: 161/161
- [PASS] H: catalog shards & zero dead master_catalog.jsonl links: 1/1
- [PASS] I: agent router triage & causal graph artifacts valid: 1/1
- [PASS] J: weekly sync crawler dry-run operational: 1/1

Audit script: scripts/audit_parity.py (read-only Ralph-Loop verifier).
