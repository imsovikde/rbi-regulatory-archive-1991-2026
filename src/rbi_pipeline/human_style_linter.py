#!/usr/bin/env python3
"""Human developer prose linter for markdown documentation and indexes.

Enforces zero AI slop, zero em/en dashes, zero 'not X, but Y' contrasts,
and zero chatbot filler across generated markdown files and agent guides.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

BANNED_WORDS = [
    "delve", "tapestry", "testament", "pivotal", "crucial", "landscape",
    "intricate", "meticulous", "underscores", "showcases", "fostering",
    "groundbreaking", "unparalleled", "synergy", "holistic", "paradigm",
    "game-changer", "moreover", "furthermore", "in conclusion", "robust",
    "seamless", "comprehensive",
]

NOT_X_BUT_Y_PATTERNS = [
    re.compile(r"\bnot\s+just\b.+?\bbut\b", re.IGNORECASE),
    re.compile(r"\bnot\s+merely\b.+?\bbut\b", re.IGNORECASE),
    re.compile(r"\bnot\s+only\b.+?\bbut\b", re.IGNORECASE),
    re.compile(r"\bit\s+is\s+not\b.+?;\s*it\s+is\b", re.IGNORECASE),
]

CHATBOT_FILLER_PATTERNS = [
    re.compile(r"\bhere\s+is\s+a\s+breakdown\b", re.IGNORECASE),
    re.compile(r"\blet'?s\s+dive\s+in\b", re.IGNORECASE),
    re.compile(r"\bin\s+this\s+repository,\s*we\s+will\s+explore\b", re.IGNORECASE),
    re.compile(r"\bwelcome\s+to\s+the\s+ultimate\b", re.IGNORECASE),
]

DEFAULT_TARGETS = [
    "README.md",
    "INDEX.md",
    "llms.txt",
    "llms-full.txt",
]


def lint_text(text: str, filename: str = "") -> list[str]:
    violations: list[str] = []
    lines = text.splitlines()

    for idx, line in enumerate(lines, 1):
        # 1. Em dash (\u2014) and En dash (\u2013)
        if "\u2014" in line:
            violations.append(f"{filename}:{idx}: contains em dash (\\u2014). Use comma, colon, or hyphen instead.")
        if "\u2013" in line:
            violations.append(f"{filename}:{idx}: contains en dash (\\u2013). Use hyphen (-) instead.")

        # 2. AI slop vocabulary
        for word in BANNED_WORDS:
            # Check for word boundary match
            if re.search(r"\b" + re.escape(word) + r"\b", line, re.IGNORECASE):
                violations.append(f"{filename}:{idx}: contains banned AI vocabulary '{word}'")

        # 3. Not X but Y patterns
        for pat in NOT_X_BUT_Y_PATTERNS:
            if pat.search(line):
                violations.append(f"{filename}:{idx}: contains 'not X, but Y' contrast pattern: {pat.pattern}")

        # 4. Chatbot filler
        for pat in CHATBOT_FILLER_PATTERNS:
            if pat.search(line):
                violations.append(f"{filename}:{idx}: contains chatbot filler pattern: {pat.pattern}")

    return violations


def lint_file(path: str) -> list[str]:
    if not os.path.exists(path):
        return [f"{path}: file does not exist"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as exc:
        return [f"{path}: failed to read: {exc}"]
    return lint_text(text, filename=path)


def collect_target_files(repo_root: str, explicit_paths: list[str] | None = None) -> list[str]:
    if explicit_paths:
        return explicit_paths

    targets: list[str] = []
    for rel in DEFAULT_TARGETS:
        full = os.path.join(repo_root, rel)
        if os.path.exists(full):
            targets.append(full)

    router_dir = os.path.join(repo_root, "index", "agent_router")
    if os.path.isdir(router_dir):
        for name in sorted(os.listdir(router_dir)):
            if name.endswith(".md"):
                targets.append(os.path.join(router_dir, name))

    return targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="specific files to lint (default: README, INDEX, llms, router)")
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    files = collect_target_files(repo_root, args.paths if args.paths else None)

    all_violations: list[str] = []
    for f in files:
        violations = lint_file(f)
        all_violations.extend(violations)

    if all_violations:
        print(f"FAILED: {len(all_violations)} human style violation(s) found across {len(files)} file(s):")
        for v in all_violations:
            print(f"  {v}")
        return 1

    print(f"PASS: {len(files)} file(s) checked with zero human style violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
