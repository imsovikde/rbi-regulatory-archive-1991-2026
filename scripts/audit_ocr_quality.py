"""Feature F32: OCR Quality and Mojibake Sentinel.

Calculates text character entropy and replacement character ratios across
Markdown files to audit text readability and identify potential mojibake.
"""

from __future__ import annotations

import argparse
import glob
import math
import os
from collections import Counter


def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    entropy = -sum((cnt / total) * math.log2(cnt / total) for cnt in counts.values())
    return entropy


def audit_ocr_quality(repo_root: str, sample_limit: int = 200) -> dict:
    sample_files = glob.glob(os.path.join(repo_root, "data", "**", "*.md"), recursive=True)[:sample_limit]
    
    total_audited = 0
    high_quality_count = 0
    mojibake_count = 0
    entropies = []

    for fpath in sample_files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if not content.strip():
                continue
            total_audited += 1
            
            # Check replacement characters and strange symbols
            replacement_char_ratio = content.count("\ufffd") / max(1, len(content))
            entropy = calculate_entropy(content)
            entropies.append(entropy)

            # Standard clean English/Hindi text entropy ranges from 3.5 to 5.2 bits/char
            if replacement_char_ratio > 0.05 or entropy > 6.0:
                mojibake_count += 1
            else:
                high_quality_count += 1
        except Exception:
            continue

    avg_entropy = sum(entropies) / len(entropies) if entropies else 0.0
    quality_score = (high_quality_count / total_audited * 100.0) if total_audited else 100.0

    return {
        "files_audited": total_audited,
        "high_quality_files": high_quality_count,
        "flagged_mojibake_files": mojibake_count,
        "mean_character_entropy": round(avg_entropy, 3),
        "ocr_quality_pass_rate_pct": round(quality_score, 2),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100)
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    metrics = audit_ocr_quality(repo_root, sample_limit=args.samples)
    print("OCR Quality & Mojibake Audit Results:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
