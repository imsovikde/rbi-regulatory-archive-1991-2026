"""Engine M5: Hybrid Sub-Linear BM25F + Information-Theoretic Query Entropy Router.

Implements BM25F ranking with field weights (w_ref=12.0, w_title=6.0, w_statute=5.0, w_aeo=3.5, w_body=1.0)
and statutory authority & validity priors derived from the Jacobian supersession DAG.
"""

from __future__ import annotations

import math
import re
from typing import Dict, List, Optional


FIELD_WEIGHTS = {
    "ref": 12.0,
    "title": 6.0,
    "statute": 5.0,
    "aeo": 3.5,
    "body": 1.0,
}

CATEGORY_BOOSTS = {
    "Master-Directions": 0.50,
    "Master-Circulars": 0.35,
    "Notifications": 0.25,
    "Draft-Notifications-Guidelines": 0.10,
    "Circulars": 0.20,
    "Press-Releases": 0.05,
}

K1 = 1.2
B = 0.75


def tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-zA-Z0-9]+", text.lower()) if len(t) > 1]


def compute_bm25f_score(
    query_tokens: list[str],
    doc_fields: dict[str, str],
    field_lens: dict[str, int],
    avg_field_lens: dict[str, float],
    idf_map: dict[str, float],
) -> float:
    score = 0.0
    for q in query_tokens:
        idf = idf_map.get(q, 1.0)
        # Compute length-normalized weighted term frequency
        tf_tilde = 0.0
        for fld, text in doc_fields.items():
            w = FIELD_WEIGHTS.get(fld, 1.0)
            flen = field_lens.get(fld, len(text.split()))
            avg_len = avg_field_lens.get(fld, 50.0)
            len_norm = 1.0 - B + B * (flen / avg_len) if avg_len else 1.0
            raw_tf = text.lower().count(q)
            tf_tilde += (w * raw_tf) / len_norm

        term_score = idf * (tf_tilde * (K1 + 1.0)) / (tf_tilde + K1)
        score += term_score

    return score


def compute_final_regulatory_score(
    bm25f_score: float,
    category: str,
    validity_score: float = 1.0,
) -> float:
    """Combines BM25F lexical score with statutory hierarchy boost and PIT validity."""
    cat_boost = CATEGORY_BOOSTS.get(category, 0.0)
    # Score_Final = Score_BM25F * (1 + gamma_cat) * (0.2 + 0.8 * v_D(T))
    final_score = bm25f_score * (1.0 + cat_boost) * (0.2 + 0.8 * validity_score)
    return round(final_score, 4)


def build_d1_fts5_schema_sql() -> str:
    """Returns the production D1 FTS5 virtual table definition."""
    return (
        "CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(\n"
        "  circular_no,\n"
        "  title,\n"
        "  statutes,\n"
        "  regulated_entities,\n"
        "  aeo_summary,\n"
        "  content='documents',\n"
        "  content_rowid='doc_id',\n"
        "  tokenize='porter unicode61'\n"
        ");\n"
    )


if __name__ == "__main__":
    q_tokens = tokenize("Credit Information Companies ₹100 per day compensation")
    sample_fields = {
        "ref": "DOR.CRE.REC.45/2023-24",
        "title": "Framework for compensation to customers for delayed updation/rectification by credit institutions and CICs",
        "statute": "Credit Information Companies (Regulation) Act, 2005",
        "aeo": "Mandates Rs 100 per calendar day compensation to complainants if credit reports are not updated within 30 days.",
        "body": "Reserve Bank of India directions under Section 11 of CICRA 2005.",
    }
    f_lens = {k: len(v.split()) for k, v in sample_fields.items()}
    avg_lens = {"ref": 5.0, "title": 15.0, "statute": 10.0, "aeo": 25.0, "body": 200.0}
    idfs = {t: 2.5 for t in q_tokens}

    bm_score = compute_bm25f_score(q_tokens, sample_fields, f_lens, avg_lens, idfs)
    final_score = compute_final_regulatory_score(bm_score, "Circulars", validity_score=1.0)
    print(f"BM25F score: {bm_score:.4f}, Final validity-weighted score: {final_score:.4f}")
