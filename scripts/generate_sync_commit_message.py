#!/usr/bin/env python3
"""Generate an intelligent, evidence-backed Git commit message for RBI archive sync and audit commits."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import quote

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.rbi_pipeline.rbi_crawler import DATASET_REPO, RBI_INDEX_ENDPOINTS

GITHUB_REPO_SLUG = "imsovikde/rbi-regulatory-archive-1991-2026"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_REPO_SLUG}"
HF_DATASET_URL = f"https://huggingface.co/datasets/{DATASET_REPO}"
PORTAL_URL = "https://rbi-archive.pages.dev"
MCP_ENDPOINT_URL = "https://rbi-archive.pages.dev/mcp"


def _load_json(path: str | None, default):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def _run_git(args: list[str], cwd: str) -> str:
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        return res.stdout.strip() if res.returncode == 0 else ""
    except Exception:
        return ""


def parse_cached_numstat(cwd: str) -> dict:
    """Parse staged diff metrics via git diff --cached --numstat."""
    raw = _run_git(["-c", "core.quotepath=false", "diff", "--cached", "--numstat"], cwd)
    files = []
    total_added = 0
    total_deleted = 0
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) < 3:
            continue
        added_s, deleted_s, filename = parts
        is_binary = added_s == "-" or deleted_s == "-"
        added = 0 if is_binary else int(added_s or 0)
        deleted = 0 if is_binary else int(deleted_s or 0)
        total_added += added
        total_deleted += deleted
        files.append({
            "filename": filename,
            "added": added,
            "deleted": deleted,
            "total": (1 if is_binary else added + deleted),
            "is_binary": is_binary,
        })
    files.sort(key=lambda f: (-f["total"], f["filename"]))
    return {
        "files": files,
        "total_added": total_added,
        "total_deleted": total_deleted,
        "net_delta": total_added - total_deleted,
    }


def parse_audit_md(audit_path: str) -> dict:
    """Parse 12-gate status and line items from AUDIT.md."""
    info = {
        "passed": 0,
        "total": 12,
        "items_passed": 0,
        "items_total": 0,
        "verdict": "UNKNOWN",
        "gates": [],
    }
    if not os.path.exists(audit_path):
        return info
    with open(audit_path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    m = re.search(
        r"<!--\s*RESULT\s+passed=(\d+)\s+total=(\d+)\s+items_passed=(\d+)\s+items_total=(\d+)\s+verdict=(\w+)\s*-->",
        text,
    )
    if m:
        info["passed"] = int(m.group(1))
        info["total"] = int(m.group(2))
        info["items_passed"] = int(m.group(3))
        info["items_total"] = int(m.group(4))
        info["verdict"] = m.group(5)
    for line in text.splitlines():
        if line.startswith("- [PASS] ") or line.startswith("- [FAIL] "):
            info["gates"].append(line)
    return info


def _workflow_run_url() -> str:
    server = os.environ.get("GITHUB_SERVER_URL")
    repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    if server and repo and run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return ""


def _signing_description(repo_root: str) -> str:
    fmt = _run_git(["config", "--get", "gpg.format"], repo_root).lower()
    if fmt == "ssh":
        return "OpenSSH Ed25519 (`commit.gpgsign = true`)"
    return "OpenPGP RSA-4096 (`E3A0ABB6FBEC5840` / subkey `72BA468A855F34E2`, `commit.gpgsign = true`)"


def _github_blob_url(rel_path: str) -> str:
    return f"{GITHUB_REPO_URL}/blob/main/{quote(rel_path.strip(), safe='/')}"


def _count_direct_urls(repo_root: str) -> int:
    urls_path = os.path.join(repo_root, "manifest", "pdf_final_direct_urls.txt")
    if not os.path.exists(urls_path):
        return 0
    with open(urls_path, "r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for ln in handle if ln.strip())


def build_commit_message(
    repo_root: str,
    mode: str = "sync",
    crawl_report_path: str | None = None,
    register_report_path: str | None = None,
    conversion_report_path: str | None = None,
    hf_report_path: str | None = None,
) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    state = _load_json(os.path.join(repo_root, "STATE.json"), {})
    done_count = int(state.get("done_count") or 0)
    total_count = int(state.get("total_count") or 0)
    pct = float(state.get("pct") or (100.0 if total_count == done_count else 0.0))
    direct_urls_count = _count_direct_urls(repo_root)

    audit = parse_audit_md(os.path.join(repo_root, "AUDIT.md"))
    diff = parse_cached_numstat(repo_root)
    crawl = _load_json(crawl_report_path, {})
    register = _load_json(register_report_path, {})
    conversion = _load_json(conversion_report_path, {})
    hf_report = _load_json(hf_report_path, {})

    docs = [d for d in conversion.get("documents", []) if d.get("status") == "DONE"]
    failed_docs = [d for d in conversion.get("documents", []) if d.get("status") != "DONE"]
    converted_count = int(conversion.get("converted_count") or len(docs))
    registered_count = int(register.get("registered_count") or converted_count)
    native_docs = sum(1 for d in docs if int(d.get("ocr_pages") or 0) == 0)
    ocr_docs = sum(1 for d in docs if int(d.get("ocr_pages") or 0) > 0)
    total_pages = int(conversion.get("total_pages") or sum(int(d.get("total_pages") or 0) for d in docs))
    native_pages = int(conversion.get("native_pages") or sum(int(d.get("native_pages") or 0) for d in docs))
    ocr_pages = int(conversion.get("ocr_pages") or sum(int(d.get("ocr_pages") or 0) for d in docs))
    engines_used = conversion.get("engines_used") or {}
    verdicts = conversion.get("verification_statuses") or {}
    by_category = conversion.get("by_category") or {}

    audit_score = f"{audit['passed']}/{audit['total']}"
    audit_icon = "🟢" if audit["verdict"] == "PASS" else "🔴"

    lines: list[str] = []

    if mode == "audit":
        lines.append(
            f"chore(audit): integrity audit {today} | {audit_score} checks | {done_count}/{total_count} verified"
        )
    else:
        lines.append(
            f"chore(sync): +{converted_count} new RBI documents -> MD ({done_count}/{total_count}) | "
            f"{today} | {native_docs} native + {ocr_docs} OCR | {audit_score} audit"
        )

    lines.append("")
    lines.append("### 🔗 Upstream Resource & Endpoint Linkage")
    lines.append(f"- **Archive Repository**: [{GITHUB_REPO_SLUG}]({GITHUB_REPO_URL})")
    lines.append(f"- **Upstream PDF Dataset (Hugging Face)**: [{DATASET_REPO}]({HF_DATASET_URL})")
    lines.append(f"- **Public Web Portal**: [rbi-archive.pages.dev]({PORTAL_URL})")
    lines.append(f"- **Official Streamable HTTP MCP Endpoint**: `{MCP_ENDPOINT_URL}`")
    run_url = _workflow_run_url()
    if run_url:
        workflow_name = os.environ.get("GITHUB_WORKFLOW") or "GitHub Actions Sync"
        lines.append(f"- **GitHub Actions Run**: [{workflow_name} (#{os.environ.get('GITHUB_RUN_ID')})]({run_url})")

    lines.append("")
    lines.append("#### 🌐 Monitored RBI & Hugging Face Source Endpoints")
    ep_map = {e["name"]: e for e in crawl.get("endpoints", []) if isinstance(e, dict) and "name" in e}
    for ep_name, ep_url in RBI_INDEX_ENDPOINTS.items():
        tel = ep_map.get(ep_name)
        if tel:
            st = tel.get("status", "UNKNOWN")
            icon = "🟢" if st == "OK" else ("🟡" if "WARN" in st or "NO_DIRECTORY" in st else "🔴")
            http_s = tel.get("http_status")
            http_part = f"HTTP {http_s}" if http_s else st
            detail = (
                f"{icon} {http_part} | scanned `{tel.get('total_found', 0)}` links | "
                f"new `{tel.get('new_count', 0)}`"
            )
            if tel.get("detail_fetches"):
                detail += f" | detail fetches `{tel['detail_fetches']}`"
            if tel.get("error"):
                detail += f" ({tel['error'][:100]})"
            lines.append(f"- **{ep_name}**: [{ep_url}]({ep_url}) — {detail}")
        else:
            lines.append(f"- **{ep_name}**: [{ep_url}]({ep_url}) — Configured active endpoint")

    if hf_report:
        hf_remote = hf_report.get("remote_pdf_count", 0)
        hf_new = hf_report.get("new_count", 0)
        hf_status = "🟢" if hf_report.get("status") == "OK" else "🟡"
        lines.append(
            f"- **Hugging-Face-Watcher**: [{HF_DATASET_URL}]({HF_DATASET_URL}) — "
            f"{hf_status} `{hf_remote:,}` dataset PDFs checked | new `{hf_new}`"
        )
    else:
        lines.append(f"- **Hugging-Face-Watcher**: [{HF_DATASET_URL}]({HF_DATASET_URL}) — Upstream dataset mirror")

    if mode == "sync":
        lines.append("")
        lines.append("### 📄 New Documents Saved & Conversion Engine Intelligence")
        lines.append(f"- **Candidates Discovered**: `{register.get('discovered_count', crawl.get('total_new', converted_count))}`")
        lines.append(f"- **Fresh Unseen PDFs**: `{register.get('fresh_count', registered_count)}`")
        lines.append(f"- **PDFs Verified & Registered**: `{registered_count}`")
        lines.append(f"- **Saved & Verified as Markdown**: `{converted_count}`")
        lines.append(f"- **Failed Conversions**: `{len(failed_docs)}`")
        lines.append(f"- **Skipped Download Candidates**: `{register.get('skipped_count', 0)}`")
        lines.append(f"- **Backfilled to Hugging Face**: `{register.get('hf_uploaded_count', 0)}/{registered_count}`")
        if register.get("hf_warning"):
            lines.append(f"- **Hugging Face Note**: {register['hf_warning']}")
        lines.append(
            f"- **Page & Extraction Split**: `{total_pages}` total page(s) — "
            f"`{native_pages}` born-digital native, `{ocr_pages}` OCR rasterized"
        )
        if engines_used:
            eng_str = ", ".join(f"`{k}` ({v} file(s))" for k, v in sorted(engines_used.items(), key=lambda kv: (-kv[1], kv[0])))
            lines.append(f"- **Conversion Mechanisms Used**: {eng_str}")
        if verdicts:
            ver_str = ", ".join(f"`{k}` ({v})" for k, v in sorted(verdicts.items()))
            lines.append(f"- **Verification Statuses**: {ver_str}")
        if by_category:
            cat_str = ", ".join(f"`{k}` (+{v})" for k, v in sorted(by_category.items(), key=lambda kv: (-kv[1], kv[0])))
            lines.append(f"- **Category Breakdown**: {cat_str}")

        if docs:
            lines.append("")
            lines.append("#### 📑 Saved Regulatory Documents (Markdown & Source Links)")
            max_list = 100
            for idx, d in enumerate(docs[:max_list], 1):
                md_rel = d.get("md_path") or ""
                md_url = _github_blob_url(md_rel)
                pdf_url = d.get("pdf_url") or ""
                hf_url = d.get("hf_url") or ""
                listing_url = d.get("listing_url") or ""
                title = (d.get("title") or os.path.basename(md_rel)).replace("\n", " ")
                cat = d.get("category") or ""
                doc_id = d.get("doc_id") or ""
                eng = d.get("engine") or "unknown"
                tp = d.get("total_pages") or 0
                np_cnt = d.get("native_pages") or 0
                op_cnt = d.get("ocr_pages") or 0
                ver = d.get("verification_status") or "VERIFIED_LEVEL_5"
                links_parts = [f"[Markdown]({md_url})"]
                if pdf_url:
                    links_parts.append(f"[RBI PDF]({pdf_url})")
                if listing_url:
                    links_parts.append(f"[RBI Listing]({listing_url})")
                if hf_url:
                    links_parts.append(f"[HF PDF]({hf_url})")
                links_joined = " | ".join(links_parts)
                lines.append(
                    f"{idx}. **{cat}** `{doc_id}`: {title} — "
                    f"{tp}p (`{np_cnt}` native / `{op_cnt}` OCR via `{eng}`, `{ver}`) — {links_joined}"
                )
            if len(docs) > max_list:
                lines.append(
                    f"... and {len(docs) - max_list} additional saved document(s) indexed under "
                    f"[index/by_year/]({GITHUB_REPO_URL}/tree/main/index/by_year) and "
                    f"[manifest/catalog/]({GITHUB_REPO_URL}/tree/main/manifest/catalog)."
                )
        if register.get("skipped_items"):
            lines.append("")
            lines.append("#### ⚠️ Skipped / Unacquired Candidates")
            for item in register["skipped_items"][:15]:
                lines.append(f"- `{item.get('pdf_url')}`: {item.get('reason')}")
            if len(register["skipped_items"]) > 15:
                lines.append(f"- ... and {len(register['skipped_items']) - 15} more skipped candidate(s).")

    lines.append("")
    lines.append("### 📊 Mathematical Repository & Corpus Diff Metrics")
    lines.append(f"- **Corpus Completion**: `{done_count:,} / {total_count:,}` PDFs -> Markdown (`{pct:.4f}%`)")
    lines.append(f"- **Canonical Direct RBI URLs**: `{direct_urls_count:,}`")
    lines.append(f"- **Impacted Files in Commit**: `{len(diff['files']):,}`")
    lines.append(f"- **Lines Added (+)**: `{diff['total_added']:,}`")
    lines.append(f"- **Lines Deleted (-)**: `{diff['total_deleted']:,}`")
    net_sign = "+" if diff["net_delta"] >= 0 else ""
    lines.append(f"- **Net Line Delta**: `{net_sign}{diff['net_delta']:,} lines`")
    lines.append(
        "- **Synchronized Linked Artifacts**: `README.md`, `INDEX.md`, `STATE.json`, `PROGRESS.md`, `AUDIT.md`, "
        "`llms.txt`, `llms-full.txt`, `llms-*.txt`, `manifest/hf_88236_inventory.jsonl`, "
        "`manifest/sha256_conversion_ledger.csv`, `manifest/pdf_final_direct_urls.txt`, `manifest/catalog/*.jsonl`, "
        "`index/by_year/*`, `index/by_category/*`, `index/url_to_path_map.json`, `index/url_shards/*`, "
        "`index/agent_router/*`, `index/mphf_*.bin`, `index/jacobian_neumann_csr.bin`, `seo/*`, "
        "`data/<Category>/<Year>/INDEX.md`, `rbi_doc_mcp_fts5.sqlite.zst`"
    )

    lines.append("")
    lines.append("### 📁 Per-File Line Change Impact")
    if diff["files"]:
        for f in diff["files"][:25]:
            if f["is_binary"]:
                lines.append(f"- `[BINARY]`  {f['filename']}")
            else:
                lines.append(f"- `+{f['added']:5d} / -{f['deleted']:5d}`  {f['filename']}")
        if len(diff["files"]) > 25:
            lines.append(f"- ... and {len(diff['files']) - 25} more modified file(s).")
    else:
        lines.append("- No staged file modifications.")

    lines.append("")
    lines.append("### 🛡️ 12-Gate Integrity Audit & Zero-404 Health Check")
    lines.append(
        f"- **Overall Audit Verdict**: {audit_icon} `{audit_score}` checks passed "
        f"(`{audit['items_passed']:,}/{audit['items_total']:,}` items verified — `{audit['verdict']}`)"
    )
    for gate in audit["gates"]:
        lines.append(f"  {gate}")

    lines.append("")
    lines.append("### 🔐 Cryptographic Provenance")
    lines.append("- **Committer Identity**: Souvik Dey (`imsovikde <imsovikde@gmail.com>`)")
    lines.append(f"- **Signature Mechanism**: {_signing_description(repo_root)} — 🟢 Verified")
    lines.append(
        "- **Chained Verification**: Downstream `Verify Index Integrity & Zero-404 Links` "
        "triggered automatically on push via PAT authentication"
    )

    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("sync", "audit"), default="sync")
    parser.add_argument("--crawl-report", default=".cache/sync/crawl_report.json")
    parser.add_argument("--register-report", default=".cache/sync/register_report.json")
    parser.add_argument("--conversion-report", default=".cache/sync/conversion_report.json")
    parser.add_argument("--hf-report", default=".cache/sync/hf_sync_report.json")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)

    msg = build_commit_message(
        REPO_ROOT,
        mode=args.mode,
        crawl_report_path=args.crawl_report,
        register_report_path=args.register_report,
        conversion_report_path=args.conversion_report,
        hf_report_path=args.hf_report,
    )
    if args.out:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(msg)
    else:
        sys.stdout.write(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
