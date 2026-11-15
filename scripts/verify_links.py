"""Zero-404 Index Link Verifier.

Recursively extracts every Markdown link [text](target) across README.md,
INDEX.md, and all index/**/*.md files and asserts every link resolves to an
existing file on disk with zero 404 broken targets.
"""

from __future__ import annotations

import glob
import os
import sys
import urllib.parse


def verify_all_links(repo_root: str) -> dict:
    target_files = [
        os.path.join(repo_root, "README.md"),
        os.path.join(repo_root, "INDEX.md"),
    ]
    target_files.extend(glob.glob(os.path.join(repo_root, "index", "**", "*.md"), recursive=True))

    checked_links = 0
    broken_links = []

    for md_file in target_files:
        if not os.path.exists(md_file):
            continue
        base_dir = os.path.dirname(md_file)
        with open(md_file, "r", encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, 1):
                if "](" in line:
                    pos = 0
                    while True:
                        idx = line.find("](", pos)
                        if idx == -1:
                            break
                        end_paren = line.find(")", idx + 2)
                        if end_paren == -1:
                            break
                        link_target = line[idx + 2 : end_paren].strip()
                        pos = end_paren + 1

                        # Skip external URLs or pure anchors
                        if link_target.startswith(("http://", "https://", "mailto:", "#")):
                            continue

                        # Clean anchor part if any
                        clean_target = link_target.split("#")[0]
                        if not clean_target:
                            continue

                        checked_links += 1
                        unquoted = urllib.parse.unquote(clean_target)
                        resolved_path = os.path.normpath(os.path.join(base_dir, unquoted))
                        if os.name == "nt" and not resolved_path.startswith("\\\\?\\"):
                            full_check_path = "\\\\?\\" + os.path.abspath(resolved_path)
                        else:
                            full_check_path = resolved_path

                        if not os.path.exists(full_check_path):
                            rel_source = os.path.relpath(md_file, repo_root)
                            broken_links.append(f"{rel_source}:{line_no}: target '{link_target}' does not exist on disk")
                            if len(broken_links) >= 50:
                                break
                    if len(broken_links) >= 50:
                        break

    return {
        "files_scanned": len(target_files),
        "total_links_checked": checked_links,
        "broken_links_count": len(broken_links),
        "sample_failures": broken_links[:10],
    }


if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    res = verify_all_links(repo_root)
    print(f"Scanned {res['files_scanned']} files, verified {res['total_links_checked']:,} local links.")
    if res["broken_links_count"] == 0:
        print("VERIFICATION PASS: 0 broken links found across all index files.")
        sys.exit(0)
    else:
        print(f"VERIFICATION FAIL: {res['broken_links_count']} broken links found:")
        for fail in res["sample_failures"]:
            print(f"  - {fail}")
        sys.exit(1)
