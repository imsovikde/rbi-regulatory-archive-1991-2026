"""Mathematical kernel & succinct data structures for RBI Regulatory Archive.

Engines:
- mphf_arena (Engine M1): Minimal Perfect Hash Function & [u8; 6] unaligned packed byte arena.
- elias_fano (Engine M2): Elias-Fano quasi-succinct monotone bitvector encoding.
- jacobian_dag (Engine M3): Jacobian determinant & nilpotent Neumann series on the statutory DAG.
- cdc_zstd (Engine M4): Gear rolling hash Content-Defined Chunking & trained Zstandard dictionary.
- bm25f_router (Engine M5): Hybrid sub-linear BM25F + statutory authority validity prior.
"""

from __future__ import annotations

__all__ = [
    "mphf_arena",
    "elias_fano",
    "jacobian_dag",
    "cdc_zstd",
    "bm25f_router",
]
