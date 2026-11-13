#!/usr/bin/env python3
"""Weekly integrity audit for the RBI Regulatory Archive (GitHub repo).

Checks:
  (a) every ledger DONE row has a .md file with valid YAML frontmatter,
      a pdf_sha256 matching the ledger, and an md_sha256 matching the
      SHA-256 of the Markdown body (content after the closing --- line);
  (b) counts in STATE.json match the ledger;
  (c) the last commit on main is authored by Souvik Dey <imsovikde@gmail.com>;
  (d) index/url_to_path_map.json covers every pdf_url in
      manifest/pdf_final_direct_urls.txt.

Writes AUDIT.md at the repo root and exits 0 only when every check passes.
This script only reads files. It never modifies any .md file.
"""
import csv
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "manifest", "sha256_conversion_ledger.csv")
STATE = os.path.join(ROOT, "STATE.json")
URL_MAP = os.path.join(ROOT, "index", "url_to_path_map.json")
URLS_FILE = os.path.join(ROOT, "manifest", "pdf_final_direct_urls.txt")
AUDIT = os.path.join(ROOT, "AUDIT.md")

REQUIRED_FRONTMATTER = [
    "doc_id", "title", "category", "year", "source_hf_url",
    "source_rbi_url", "pdf_sha256", "md_sha256", "total_pages",
    "verification_status",
]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def split_frontmatter(text):
    """Return (frontmatter dict, body str) or (None, text) if invalid."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    body = text[end + 5:]
    fm = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"')
    return fm, body


def check_a():
    """Ledger DONE rows vs .md files. Returns (passed, total, failures)."""
    failures = []
    total = 0
    passed = 0
    with open(LEDGER, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["status"] != "DONE":
                continue
            total += 1
            md_path = os.path.join(ROOT, row["md_path"])
            if not os.path.exists(md_path):
                failures.append(f"missing .md file: {row['md_path']}")
                continue
            with open(md_path, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8", errors="replace")
            fm, body = split_frontmatter(text)
            if fm is None:
                failures.append(f"invalid frontmatter: {row['md_path']}")
                continue
            missing = [k for k in REQUIRED_FRONTMATTER if k not in fm]
            if missing:
                failures.append(f"frontmatter missing keys {missing}: {row['md_path']}")
                continue
            if fm.get("pdf_sha256") != row["pdf_sha256"]:
                failures.append(f"pdf_sha256 mismatch: {row['md_path']}")
                continue
            if fm.get("md_sha256") != sha256_bytes(body.encode("utf-8")):
                failures.append(f"md_sha256 mismatch: {row['md_path']}")
                continue
            passed += 1
    return passed, total, failures


def check_b():
    """STATE.json counts vs ledger. Returns (passed, total, failures)."""
    failures = []
    with open(STATE, encoding="utf-8") as f:
        state = json.load(f)
    done = 0
    total = 0
    with open(LEDGER, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            if row["status"] == "DONE":
                done += 1
    if state.get("total_count") != total:
        failures.append(f"STATE total_count {state.get('total_count')} != ledger rows {total}")
    if state.get("done_count") != done:
        failures.append(f"STATE done_count {state.get('done_count')} != ledger DONE rows {done}")
    if state.get("remaining_count") != total - done:
        failures.append("STATE remaining_count != total - done")
    expected_pct = round(done / total * 100, 4) if total else 0.0
    if abs(float(state.get("pct", -1)) - expected_pct) > 0.0001:
        failures.append(f"STATE pct {state.get('pct')} != {expected_pct}")
    return (1 if not failures else 0), 1, failures


def check_c():
    """Last commit author is Souvik Dey <imsovikde@gmail.com>."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%an %ae"],
        cwd=ROOT, capture_output=True, text=True)
    got = out.stdout.strip()
    want = "Souvik Dey imsovikde@gmail.com"
    if got == want:
        return 1, 1, []
    return 0, 1, [f"last commit author is '{got}', expected '{want}'"]


def check_d():
    """url_to_path_map covers every pdf_url in pdf_final_direct_urls.txt."""
    with open(URL_MAP, encoding="utf-8") as f:
        url_map = json.load(f)
    with open(URLS_FILE, encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    missing = [u for u in urls if u not in url_map]
    if missing:
        return 0, 1, [f"{len(missing)} pdf_urls missing from url_to_path_map.json, e.g. {missing[0]}"]
    return 1, 1, []


def main():
    import datetime
    checks = [
        ("A: ledger DONE rows have valid .md files", check_a),
        ("B: STATE.json counts match ledger", check_b),
        ("C: last commit authored by Souvik Dey <imsovikde@gmail.com>", check_c),
        ("D: url_to_path_map covers every pdf_url", check_d),
    ]
    results = []
    groups_ok = 0
    items_passed = 0
    items_total = 0
    for name, fn in checks:
        try:
            passed, total, failures = fn()
        except FileNotFoundError as e:
            passed, total, failures = 0, 1, [f"missing file: {e.filename}"]
        except Exception as e:  # noqa: BLE001 - audit must report, not crash
            passed, total, failures = 0, 1, [f"check error: {e}"]
        group_ok = not failures
        if group_ok:
            groups_ok += 1
        results.append((name, passed, total, failures))
        items_passed += passed
        items_total += total
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    verdict = "PASS" if groups_ok == len(checks) else "FAIL"
    lines = []
    lines.append(f"# Integrity Audit {date} - {groups_ok}/{len(checks)} checks passed ({verdict})")
    lines.append("")
    lines.append(f"<!-- RESULT passed={groups_ok} total={len(checks)} items_passed={items_passed} items_total={items_total} verdict={verdict} -->")
    lines.append("")
    for name, passed, total, failures in results:
        mark = "PASS" if not failures else "FAIL"
        lines.append(f"- [{mark}] {name}: {passed}/{total}")
        for fail in failures[:20]:
            lines.append(f"  - {fail}")
        if len(failures) > 20:
            lines.append(f"  - ... and {len(failures) - 20} more")
    lines.append("")
    lines.append("Audit script: scripts/audit_parity.py (read-only; it never modifies .md files).")
    lines.append("")
    with open(AUDIT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"audit: {groups_ok}/{len(checks)} checks passed ({verdict}); {items_passed}/{items_total} items verified")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
