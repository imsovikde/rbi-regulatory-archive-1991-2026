# RBI Regulatory Archive 1991-2026: Agent-First Markdown

Every publicly available Reserve Bank of India regulatory PDF, 1991-2026, converted to
GitHub-Flavored Markdown with 1:1 path parity, deterministic indexes, and SHA-256
verification on every file. Built for AI agents, RAG pipelines, and legal verification.

Upstream PDFs (byte-identical source of truth):
https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026

<!-- PROGRESS-START -->
## Conversion progress

- **Total PDFs:** 88236
- **Converted to Markdown:** 88236
- **Remaining:** 0
- **Progress:** [########################################] 100.0000%

| Category | Total | Converted | Progress |
| --- | ---: | ---: | ---: |
| Master-Directions | 397 | 397 | 100.0000% |
| Notifications | 10527 | 10527 | 100.0000% |
| Master-Circulars | 1013 | 1013 | 100.0000% |
| Draft-Notifications-Guidelines | 546 | 546 | 100.0000% |
| Circulars | 11690 | 11690 | 100.0000% |
| Press-Releases | 64063 | 64063 | 100.0000% |
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

1. Read [llms.txt](llms.txt), [index/agent_router/TRIAGE_GUIDE.md](index/agent_router/TRIAGE_GUIDE.md), and [index/agent_router/AEO_REGULATORY_FAQ.md](index/agent_router/AEO_REGULATORY_FAQ.md) first. They provide the statutory hierarchy, zero-hallucination Q&A, and deterministic routing protocol in $\le 3$ tool calls.
2. For controlling law by regulated entity (Commercial Banks, NBFCs, UCBs, Payment Systems, FEMA, etc.), consult [index/agent_router/active_master_directions_by_entity.md](index/agent_router/active_master_directions_by_entity.md) or its machine-readable JSON version [index/agent_router/active_master_directions_by_entity.json](index/agent_router/active_master_directions_by_entity.json).
3. To lookup a circular by official reference number (e.g. `RBI/2024-25/123`, `DOR.No.DIR.BC...`), use [index/agent_router/circular_ref_to_path.json](index/agent_router/circular_ref_to_path.json).
4. To trace supersessions, amendments, or statutory penalties, query [index/agent_router/citation_and_consequence_graph.jsonl](index/agent_router/citation_and_consequence_graph.jsonl).
5. To resolve an RBI or Hugging Face URL without loading large files, compute `sha256(url.lower())[:2]` and read the compact 256-shard file at `index/url_shards/<hex>.json` (or the master lookup [index/url_to_path_map.json](index/url_to_path_map.json)).
6. Use [INDEX.md](INDEX.md) for master table of contents, or [llms-full.txt](llms-full.txt) for the exhaustive link map. Every directory `data/<Category>/<Year>/` also features its own local `INDEX.md`.
7. Search document metadata across [manifest/catalog/<YYYY>.jsonl](manifest/catalog/).
8. Read the Markdown file at `data/<Category>/<Year>/<stem>.md`. Its YAML frontmatter carries `doc_id`, `title`, `pdf_sha256`, `md_sha256`, `total_pages`, `native_pages`, `ocr_pages`, `conversion_engine`, and `verification_status`.

## Folder layout

```text
README.md, PROGRESS.md, STATE.json, llms.txt, llms-full.txt, INDEX.md, ARCHITECTURE.md
manifest/
  pdf_final_direct_urls.txt      81,828 direct RBI PDF URLs (canonical endpoint list)
  hf_88236_inventory.jsonl       88,236-file inventory synced from Hugging Face
  sha256_conversion_ledger.csv   PDF SHA-256, MD SHA-256, engine, pages, status per file
  catalog/<YYYY>.jsonl           Machine-readable metadata catalog for agents, one shard per year
index/
  agent_router/                  Agent routing engine & statutory hierarchy
    TRIAGE_GUIDE.md              Statutory hierarchy and <= 3 tool call retrieval protocol
    active_master_directions_by_entity.md / .json Controlling Master Directions by entity
    circular_ref_to_path.json    Circular reference number -> .md file mapping
    citation_and_consequence_graph.jsonl Causal citations, amendments, supersessions & penalties
  url_shards/                    256 compact URL shards (00.json..ff.json) for agent context safety
  by_year/                       1991.md ... 2026.md (per-year Markdown indexes)
  by_category/                   One Markdown index per category (Master-Directions, Notifications, etc.)
  url_to_path_map.json           O(1) URL -> .md path master lookup
  url_collisions.json            RBI URLs that map to more than one document
data/                            Converted Markdown, with per-directory INDEX.md for all 161 folders
src/rbi_pipeline/                converter, crawler, indexer, statutory_indexer, runner, verifier
.github/workflows/               00 bootstrap, 01 conversion, 02 weekly sync, 02 fallback sync, 03 audit
scripts/                         audit_parity.py, register_new_documents.py, hf_scheduled_sync.py
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

## Web Portal, Model Context Protocol (MCP) Server & Local CLI (`npx rbi-doc-mcp --local`)

[![Public Web Portal](https://img.shields.io/badge/Web_Portal-https%3A%2F%2Frbi--archive.pages.dev-blue.svg)](https://rbi-archive.pages.dev)
[![Official MCP Endpoint](https://img.shields.io/badge/MCP_Endpoint-https%3A%2F%2Frbi--archive.pages.dev%2Fmcp-green.svg)](https://rbi-archive.pages.dev/mcp)
[![npm CLI Package](https://img.shields.io/npm/v/rbi-doc-mcp.svg?label=npx%20rbi-doc-mcp%20--local)](https://www.npmjs.com/package/rbi-doc-mcp)
[![Complete MCP Guide](https://img.shields.io/badge/Documentation-mcp--guide.md-amber.svg)](./mcp-guide.md)

AI agents, code editors (Claude, Cursor, VS Code, Windsurf), legal research pipelines, and developer terminals can query the complete 88,236-document Reserve Bank of India regulatory corpus over the official Streamable HTTP MCP server, the interactive web terminal, or the local `npx` CLI:

| Surface | Canonical Endpoint / Command | Description |
| :--- | :--- | :--- |
| Public Web Portal & Interactive Terminal | [https://rbi-archive.pages.dev](https://rbi-archive.pages.dev) | Browser-based BM25F search, statutory graph explorer, point-in-time validity checker, and court citation generator |
| Official Streamable HTTP MCP Server | `https://rbi-archive.pages.dev/mcp` | Remote MCP 2025-06-18 endpoint exposing all 8 regulatory tools, Code Mode (`rbi_doc_execute_code`), and OAuth 2.1 + PKCE |
| Local Stdio MCP Server & CLI (`npm`) | `npx rbi-doc-mcp --local` | Offline-capable local `stdio` MCP server and terminal CLI using cached static BM25F shards and GitHub Raw / Hugging Face mirrors |
| User Account & Usage Dashboard | [https://rbi-archive.pages.dev/account](https://rbi-archive.pages.dev/account) | Usage analytics (24h / 7d / 30d), active OAuth client sessions, and one-click session revocation |
| Complete MCP Connection & Tool Guide | [mcp-guide.md](./mcp-guide.md) ([Full GitHub URL](https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/blob/main/mcp-guide.md)) | Step-by-step setup for Claude, Cursor, VS Code, Windsurf, `npx rbi-doc-mcp --local`, access tiers, and all 8 tool schemas |

### 3-Step Quick Start

1. **Connect via Remote Streamable HTTP or Local `npx` CLI**:
   ```bash
   # Option A: Remote Streamable HTTP MCP Server
   claude mcp add --transport http rbi-archive https://rbi-archive.pages.dev/mcp

   # Option B: Local Stdio MCP Server (zero remote rate limits, local disk cache)
   npx rbi-doc-mcp --local
   ```
2. **Choose your access tier** when connecting to `https://rbi-archive.pages.dev/mcp`: click **Continue Anonymously** for instant read-only access (`30 req/min`), or sign in with a free account at [https://rbi-archive.pages.dev/account](https://rbi-archive.pages.dev/account) for `120 req/min`, multi-step Code Mode (`rbi_doc_execute_code`), and session management.
3. **Query the 88,236-document archive** from your AI assistant or directly in your terminal:
   ```bash
   npx rbi-doc-mcp --search "Know Your Customer Master Direction"
   npx rbi-doc-mcp --resolve "RBI/2017-18/15"
   npx rbi-doc-mcp --validity "rbi_081878" 2026-01-01
   ```

### Public MCP Tool Suite (8 Tools)

| Tool Name | Primary Regulatory Capability |
| :--- | :--- |
| `search_rbi_regulations` | Hybrid BM25F (`k1 = 1.2`, `b = 0.75`) and 128-dim semantic search across all 88,236 RBI documents (1991-2026) with category, year, and statute filters |
| `fetch_rbi_markdown` | Full-text retrieval of SHA-256-verified GitHub-Flavored Markdown for any RBI Master Direction, Circular, or Notification |
| `resolve_rbi_doc` | O(1) resolution of official RBI circular reference numbers (`RBI/2024-25/...`, `DOR.No...`, `DBOD.No...`), numeric IDs, or URLs into canonical metadata |
| `trace_statutory_consequences` | Causal DAG traversal of `SUPERSEDES`, `AMENDS`, `REPEALS`, and `CITES` edges, linked statutory penalties, and compliance turnaround times (TATs) |
| `verify_circular_validity` | Point-in-time legal validity verification (`ACTIVE`, `SUPERSEDED`, or `REPEALED`) on any `YYYY-MM-DD` calendar date |
| `format_court_citation` | Formal Indian judicial citation formatting with official RBI reference number, date, statutory authority, and SHA-256 digest |
| `rag_query_rbi_provisions` | Clause-level RAG over Content-Defined Chunked (CDC) statutory provisions with exact section provenance |
| `rbi_doc_execute_code` | Single-turn sandboxed JavaScript execution (`sdk.search`, `sdk.resolve`, `sdk.checkValidity`, `sdk.traceConsequences`, `sdk.cite`, `sdk.ragQuery`) |

For full parameter schemas, client JSON configurations, and example legal/compliance prompts, read the **[Complete MCP Connection & Tool Guide (mcp-guide.md)](./mcp-guide.md)**.

---

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


<!-- DYNAMIC_STATS_START -->
### Live Dynamic Archive Statistics

- **Total Regulatory Documents:** 88,236
- **Temporal Range:** 1992 through 2026
- **Conversion Progress:** 100.0000% complete

| Category | Document Count | Format |
| --- | ---: | --- |
| Press-Releases | 64,063 | GitHub-Flavored Markdown |
| Circulars | 11,690 | GitHub-Flavored Markdown |
| Notifications | 10,527 | GitHub-Flavored Markdown |
| Master-Circulars | 1,013 | GitHub-Flavored Markdown |
| Draft-Notifications-Guidelines | 546 | GitHub-Flavored Markdown |
| Master-Directions | 397 | GitHub-Flavored Markdown |
<!-- DYNAMIC_STATS_END -->
