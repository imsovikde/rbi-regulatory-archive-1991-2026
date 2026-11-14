# RBI Regulatory Archive 1991-2026: Agent-First Markdown

Every publicly available Reserve Bank of India regulatory PDF, 1991-2026, converted to
GitHub-Flavored Markdown with 1:1 path parity, deterministic indexes, and SHA-256
verification on every file. Built for AI agents, RAG pipelines, and legal verification.

Upstream PDFs (byte-identical source of truth):
https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026

<!-- PROGRESS-START -->
## Conversion progress

- **Total PDFs:** 88236
- **Converted to Markdown:** 82622
- **Remaining:** 5614
- **Progress:** [#####################################---] 93.6375%

| Category | Total | Converted | Progress |
| --- | ---: | ---: | ---: |
| Master-Directions | 397 | 397 | 100.0000% |
| Notifications | 10527 | 10527 | 100.0000% |
| Master-Circulars | 1013 | 1013 | 100.0000% |
| Draft-Notifications-Guidelines | 546 | 546 | 100.0000% |
| Circulars | 11690 | 11690 | 100.0000% |
| Press-Releases | 64063 | 58449 | 91.2368% |
<!-- PROGRESS-END -->
## What this repository is

- **88,236 RBI PDFs** (1992-2026 inventoried; the archive spans 1991-2026 and 1991 has
  no inventoried PDFs) converted to Markdown, one `.md` file per PDF, at
  `data/<Category>/<Year>/<exact PDF stem>.md`, in the exact same folder and year
  hierarchy as the Hugging Face dataset. File stems are never renamed or truncated.
- **92,100-entry census**: 88,236 PDFs plus 3,864 BLOCKED entries for which RBI serves
  no PDF. Blocked entries are listed, never hidden and never fabricated.
- **Agent-first indexing**: `llms.txt`, `llms-full.txt`, `INDEX.md`, per-year and
  per-category indexes, and `index/url_to_path_map.json` for O(1) lookup from any RBI
  or Hugging Face URL to its Markdown file.
- **Verified provenance**: every commit is authored by Souvik Dey
  <imsovikde@gmail.com> and GPG-signed, so GitHub shows the green Verified badge.
  No bot commits, ever.

## How agents should use this repository

1. Read [llms.txt](llms.txt) first. It is the concise entry-point map.
2. Use [INDEX.md](INDEX.md) for counts and navigation, or [llms-full.txt](llms-full.txt)
   for the exhaustive link map (every category, every year 1991-2026).
3. To resolve one document from a URL, look it up in
   [index/url_to_path_map.json](index/url_to_path_map.json). It maps every RBI direct
   URL (81,828 unique) and every Hugging Face resolve URL (88,236) to its `.md` path.
   A few RBI URLs (5,951) point at more than one document; those are listed in
   [index/url_collisions.json](index/url_collisions.json).
4. To search by headline or document ID, read
   [manifest/catalog/<YYYY>.jsonl](manifest/catalog/).
5. Read the Markdown file at `data/<Category>/<Year>/<stem>.md`. Its YAML frontmatter
   carries `pdf_sha256`, `md_sha256`, `total_pages`, `native_pages`, `ocr_pages`,
   `conversion_engine`, and `verification_status`.

## How to verify a file

```bash
# 1. The Markdown body hash: hash everything after the closing --- of the frontmatter
python3 -c "import hashlib; t=open('data/Notifications/2024/example.md').read(); body=t.split('\n---\n', 1)[1]; print(hashlib.sha256(body.encode()).hexdigest())"
# Compare with md_sha256 in the frontmatter.

# 2. The source PDF hash: download the PDF from source_hf_url and compare
#    its SHA-256 with pdf_sha256 in the frontmatter.
```

The weekly audit workflow (`.github/workflows/03_integrity_audit.yml`) does this for
every converted file and publishes the result in `AUDIT.md`.

## Folder layout

```text
README.md, PROGRESS.md, STATE.json, llms.txt, llms-full.txt, INDEX.md, ARCHITECTURE.md
manifest/
  pdf_final_direct_urls.txt      81,828 direct RBI PDF URLs (canonical endpoint list)
  hf_88236_inventory.jsonl       88,236-file inventory synced from Hugging Face
  sha256_conversion_ledger.csv   PDF SHA-256, MD SHA-256, engine, pages, status per file
  catalog/<YYYY>.jsonl           Machine-readable metadata catalog for agents, one shard per year
index/
  by_year/                       1991.md ... 2026.md (per-year Markdown indexes)
  by_category/                   One Markdown index per category
  url_to_path_map.json           O(1) URL -> .md path lookup
  url_collisions.json            RBI URLs that map to more than one document
data/                            Converted Markdown, same folders and years as Hugging Face
src/rbi_pipeline/                converter, crawler, indexer, runner, verifier
.github/workflows/               00 bootstrap, 01 conversion, 02 weekly sync, 03 audit
scripts/                         audit_parity.py, setup_verified_signing.sh
```

## Conversion stack

| Layer | Component | Canonical link | Role |
| --- | --- | --- | --- |
| Upstream archive | RBI Regulatory Archive (HF) | https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026 | Source of truth: 88,236 untouched RBI PDFs |
| Tier 1: native PDF to Markdown | Firecrawl AnyDoc | https://github.com/firecrawl/anydoc | Primary structural converter; raises NeedsOcr on scanned pages |
| Tier 1B: PDF inspector | Firecrawl PDF Inspector | https://github.com/firecrawl/pdf-inspector | Classifies pages (text, scanned, mixed) and pinpoints OCR pages |
| Tier 1C: PDF engine | PyMuPDF | https://github.com/pymupdf/PyMuPDF | Page rasterization, font inspection, page count verification |
| Tier 2A: primary OCR | PaddleOCR (PP-OCRv5) | https://github.com/PaddlePaddle/PaddleOCR | Neural text detection and recognition for scanned pages |
| Tier 2B: runtime | PaddlePaddle | https://github.com/PaddlePaddle/Paddle | CPU execution backend for PaddleOCR |
| Tier 2C: orchestrator | PaddleX | https://github.com/PaddlePaddle/PaddleX | Unified inference pipeline, layout and table recovery |
| Tier 2D: ONNX OCR | RapidOCR | https://github.com/RapidAI/RapidOCR | PP-OCRv5 models over ONNX Runtime, low memory |
| Tier 2E: CPU inference | ONNX Runtime | https://github.com/microsoft/onnxruntime | CPU execution accelerator |
| Tier 3A: searchable PDF | OCRmyPDF | https://github.com/ocrmypdf/OCRmyPDF | Deskew, clean, inject searchable text layer |
| Tier 3B: secondary OCR | Tesseract OCR | https://github.com/tesseract-ocr/tesseract | Secondary engine for clean scans, bilingual headers |
| Tier 3C: language data | Tesseract tessdata | https://github.com/tesseract-ocr/tessdata | eng, hin, osd trained data |
| Tier 4A: image prep | Pillow | https://github.com/python-pillow/Pillow | Thresholding, contrast, image buffers |
| Tier 4B: PDF interpreter | Ghostscript | https://github.com/ArtifexSoftware/ghostpdl | PDF/A normalization, corrupted stream repair |
| Tier 4C: PDF utilities | Poppler | https://poppler.freedesktop.org/ | pdftotext, pdfinfo, pdftoppm cross-checks |
| Tier 5A: math verification | SymPy | https://github.com/sympy/sympy | Formula parse verification |
| Tier 5B: glyph fidelity | DejaVu Fonts | https://github.com/dejavu-fonts/dejavu-fonts | Unicode coverage (₹, math operators) |

### Excluded (never used as a truth source)

- **Docling** (https://github.com/docling-project/docling): excluded as a ground-truth
  text source because of layout-induced text mutation risks on statutory documents.
- **MinerU** (https://github.com/opendatalab/MinerU): not used for truth parsing.
  The pipeline relies strictly on firecrawl/anydoc plus PP-OCRv5 / RapidOCR / Tesseract.

## Verified commit identity

Every commit in this repository is authored by **Souvik Dey <imsovikde@gmail.com>**
(`imsovikde`) and cryptographically signed with the owner's GPG key, so GitHub renders
the green Verified badge. Commits by `github-actions[bot]` or any other account are
forbidden.

- GPG key: **E3A0ABB6FBEC5840**, RSA 4096, fingerprint
  `6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840`, expires 2028-11-12.
- Proven secrets (exactly three): `GH_PAT`, `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`.
- `GH_PAT` is a fine-grained PAT scoped to this repo only, Contents read/write,
  90-day expiry. It has **no Workflows or Actions scope**, so workflows cannot push
  changes to `.github/workflows/` and cannot dispatch workflows with it. Workflow
  files are therefore updated through the GitHub web UI, never by a workflow run.
- Self-chaining uses `GITHUB_TOKEN` for the `gh workflow run` dispatch only. A
  `workflow_dispatch` event triggered by `GITHUB_TOKEN` does start a new run, and the
  new run still commits as imsovikde because the runner signs with the GPG key and
  pushes with `GH_PAT`.
- `HF_TOKEN` does not exist in GitHub secrets. Conversion reads the public Hugging
  Face dataset with no token. `HF_TOKEN` is needed only for the weekly workflow's
  Hugging Face backfill step; until it is added, that step logs a warning and skips.

## Workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `00_bootstrap.yml` | Manual dispatch | Lands the pipeline bundle from Hugging Face, then starts conversion |
| `01_continuous_conversion.yml` | Manual dispatch + every 6h watchdog | Self-chaining batch conversion until 100.0000% |
| `02_weekly_rbi_hf_github_sync.yml` | Mondays 02:30 UTC + manual | Weekly RBI crawl, HF backfill, new-document conversion |
| `03_integrity_audit.yml` | Sundays 03:00 UTC + manual | Parity, hash, author, and URL-map audit; publishes AUDIT.md |

## Known limits

- **Repository size**: the converted Markdown corpus will be large (tens of GB at
  most if every PDF converts at roughly its current size; the exact projection is to
  be filled in from the converter pilot run, and this section updated then). Pushes
  stay under GitHub's 2 GB packfile limit because conversion commits in micro-batches
  of 50-100 files.
- **Runner time limit**: GitHub Actions kills a job after 6 hours. The conversion
  workflow budgets 290 minutes (4h 50m) per run and self-chains the next run.
- **HF_TOKEN missing**: the weekly sync cannot backfill new PDFs to Hugging Face
  until the owner adds `HF_TOKEN` as a repo secret. RBI-direct conversion continues
  regardless.
- **Rate limits**: Hugging Face and GitHub API calls use exponential backoff with
  jitter. The runner paces pushes at least 5 seconds apart.
- **1991**: the inventory contains no PDFs dated 1991; the earliest year is 1992.
  The 1991 index files exist but are empty by design.
- **Duplicate RBI URLs**: 5,951 direct RBI URLs are listed for more than one
  document (same PDF listed twice, for example as both a Master Direction and a
  Notification). `url_to_path_map.json` maps each such URL to its first path in
  sorted order; all paths are in `url_collisions.json`.

## License and attribution

The documents in this archive are public publications of the Reserve Bank of India;
no copyright is claimed over them. This repository is not affiliated with, endorsed
by, or connected to the Reserve Bank of India. The conversion pipeline, indexes, and
manifests are provided as-is, without warranty.
