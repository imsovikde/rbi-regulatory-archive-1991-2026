# RBI Regulatory Archive 1991-2026: Master Index

Agent-first Markdown conversion of every publicly available Reserve Bank of India
regulatory PDF, 1991-2026. Each PDF maps 1:1 to a Markdown file at
`data/<Category>/<Year>/<exact PDF stem>.md` with the same folder and year hierarchy
as the upstream Hugging Face dataset.

Upstream PDFs: https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026

## Progress

**0 / 88,236 converted (0.0000%).** Live progress: [PROGRESS.md](PROGRESS.md).
Conversion runs in micro-batches of 50-100 PDFs per Verified commit by Souvik Dey.

## Contents by category

| Category | PDFs | Converted | Pending | Index |
| --- | ---: | ---: | ---: | --- |
| Master-Directions | 397 | 0 | 397 | [index/by_category/Master-Directions.md](index/by_category/Master-Directions.md) |
| Notifications | 10527 | 0 | 10527 | [index/by_category/Notifications.md](index/by_category/Notifications.md) |
| Master-Circulars | 1013 | 0 | 1013 | [index/by_category/Master-Circulars.md](index/by_category/Master-Circulars.md) |
| Draft-Notifications-Guidelines | 546 | 0 | 546 | [index/by_category/Draft-Notifications-Guidelines.md](index/by_category/Draft-Notifications-Guidelines.md) |
| Circulars | 11690 | 0 | 11690 | [index/by_category/Circulars.md](index/by_category/Circulars.md) |
| Press-Releases | 64063 | 0 | 64063 | [index/by_category/Press-Releases.md](index/by_category/Press-Releases.md) |
| **Total** | **88236** | **0** | **88236** | |

Inventory census: 92,100 entries. 88,236 have a PDF; 3,864 are BLOCKED (RBI serves no
PDF for them) and are listed in `manifest/master_catalog.jsonl` with status BLOCKED.
No PDF is ever invented. Years with inventoried PDFs: 1992-2026 (1991 has none).

## Contents by year

Per-year indexes live in [index/by_year/](index/by_year/): `1991.md` through `2026.md`.

## How to find a document

1. Start at [llms.txt](llms.txt) for the concise map, or [llms-full.txt](llms-full.txt) for every link.
2. Have an RBI URL or a Hugging Face URL? Look it up in [index/url_to_path_map.json](index/url_to_path_map.json) (O(1)).
3. Have a headline or document ID? Search [manifest/master_catalog.jsonl](manifest/master_catalog.jsonl).
4. Verify a file: recompute SHA-256 of the Markdown body and compare with `md_sha256` in its frontmatter; recompute the source PDF hash against `pdf_sha256`.

## Layout

```
README.md, PROGRESS.md, STATE.json, llms.txt, llms-full.txt, INDEX.md, ARCHITECTURE.md
manifest/  (inventory, conversion ledger, master catalog, 81,828 direct RBI URLs)
index/     (by_year/, by_category/, url_to_path_map.json, url_collisions.json)
data/      (converted Markdown, same folders and years as the Hugging Face dataset)
src/rbi_pipeline/  (converter, crawler, indexer, runner, verifier)
.github/workflows/  (00 bootstrap, 01 conversion, 02 weekly sync, 03 audit)
scripts/   (audit_parity.py, setup_verified_signing.sh)
```
