# Architecture: RBI Regulatory Archive Markdown Conversion Pipeline

## 1. Purpose

Turn 88,236 RBI PDFs (upstream: Hugging Face dataset
`imsovikde/rbi-regulatory-archive-1991-2026`) into GitHub-Flavored Markdown in this
repository, with 1:1 path parity, deterministic indexes for AI agents, SHA-256
verification on every file, and commits that are always authored by Souvik Dey
<imsovikde@gmail.com> and GPG-signed (green Verified badge). Then keep the repository
in sync with new RBI publications forever, weekly, with no human in the loop.

## 2. Data flow

```text
RBI website (rbi.org.in / rbidocs.rbi.org.in)
        |
        |  crawl (weekly) + historical inventory (92,100 rows)
        v
Hugging Face dataset (88,236 PDFs, byte-identical, public, no token needed to read)
        |
        |  HF resolve URLs, streamed in micro-batches, 429/5xx backoff + jitter
        v
Runner (src/rbi_pipeline/runner.py) on GitHub Actions ubuntu-latest
        |
        +--> Stage 1 pre-check: pdf_sha256, page count (PyMuPDF + pdfinfo),
        |    Ghostscript repair of broken 1990s xref tables into a temp buffer
        +--> Stage 2 anydoc native extraction + per-page char density audit
        |    (pages with < 30 alphanumeric chars and raster images -> NEEDS_OCR)
        +--> Stage 3 hybrid OCR (scanned/mixed only):
        |      Path A: OCRmyPDF + RapidOCR/Tesseract -> searchable PDF -> anydoc
        |      Path B: PyMuPDF 300 DPI raster + PaddleOCR PP-OCRv5 / PP-StructureV3
        |    Merge native + OCR pages in exact page order with <!-- PAGE N --> anchors
        +--> Stage 4 verification: page parity 1..N, SymPy formula check,
        |    GFM table pipe balance, non-empty text density on all pages
        +--> Stage 5 frontmatter + atomic write of data/<Category>/<Year>/<stem>.md
        |
        v
Ledger + indexes + STATE.json + PROGRESS.md + README.md (rebuilt every batch)
        |
        v
Verified micro-batch commit (50-100 files) + push, then self-chain while work remains
```

## 3. Module map (src/rbi_pipeline/)

| Module | Responsibility |
| --- | --- |
| `hf_enumerator.py` | Lists and streams PDFs from the Hugging Face dataset under rate limits; resumes from STATE.json |
| `rbi_crawler.py` | Crawls live RBI index endpoints; reconciles against manifest/pdf_final_direct_urls.txt; discovers new documents; backfills new PDFs to Hugging Face when HF_TOKEN is set |
| `converter.py` | The 5-stage hybrid converter (anydoc + PP-OCRv5 / RapidOCR / OCRmyPDF / Tesseract) |
| `verifier.py` | Page parity, SymPy formula check, SHA-256, GFM table validation, frontmatter validation |
| `indexer.py` | Rebuilds llms.txt, llms-full.txt, INDEX.md, per-year/per-category indexes, manifest/catalog/<YYYY>.jsonl shards, url_to_path_map.json, README.md progress section, STATE.json |
| `runner.py` | Batch loop: enumerate next pending files, convert with a worker pool, verify, commit + push per batch, enforce the 290-minute budget, write STATE.json |
| `git_committer.py` | Rate-limit-safe Verified committer: stages, commits with `git commit -S`, paces pushes (>= 5 s apart), pull --rebase + push with retry |

Supporting scripts: `scripts/audit_parity.py` (weekly read-only audit),
`scripts/setup_verified_signing.sh` (local one-command signing setup).

## 4. Batch and commit protocol

1. The runner reads `STATE.json` (`done_count`, `done_paths`, `last_batch`) and
   takes the next `BATCH_SIZE` pending rows from `manifest/sha256_conversion_ledger.csv`
   (default 75, allowed 50-100).
2. It streams each PDF from Hugging Face (resolve URL), converts it, verifies it,
   and writes `data/<Category>/<Year>/<stem>.md` with YAML frontmatter.
3. It appends the batch to the ledger (status DONE, md_sha256, page counts, engine,
   timestamp), updates `STATE.json`, `PROGRESS.md`, the README.md progress section,
   and the affected index files.
4. It commits, as Souvik Dey with `git commit -S`, with the exact message format:
   `chore(convert): [XX.XXXX%] <done>/<total> PDFs -> MD | <Category>/<Year> Batch #<N> | <native_count> anydoc + <ocr_count> OCR verified`
5. It pushes with `git pull --rebase origin main && git push origin HEAD:main`, then
   waits at least 5 seconds before the next push.
6. Batches are idempotent: a re-run skips every ledger row already DONE, so a
   killed run resumes cleanly from `STATE.json` with no duplicate work.

## 5. Self-chain protocol (rate-limit-safe continuous running)

- One workflow run has a hard 6-hour GitHub limit. The runner enforces a
  290-minute (4h 50m) budget: at the budget it flushes the current batch, commits,
  and stops cleanly.
- The workflow's final step (`if: always()`) reads `STATE.json: remaining_count`.
  While it is above 0 it dispatches the next run with
  `gh workflow run 01_continuous_conversion.yml --ref main`.
- The dispatch uses `GITHUB_TOKEN`, not the owner's PAT. Reason: the PAT
  (`GH_PAT`) is fine-grained with Contents scope only; it has no Actions scope and
  cannot dispatch workflows. A `workflow_dispatch` event fired by `GITHUB_TOKEN`
  does start a new run. The new run still commits as imsovikde because the runner
  signs with the owner's GPG key and pushes with `GH_PAT`.
- `concurrency: group rbi-markdown-conversion-pipeline, cancel-in-progress: false`
  guarantees runs never overlap and never cancel each other.
- A schedule watchdog (`15 */6 * * *`) restarts the pipeline if a self-chain
  dispatch is ever lost.
- Expected run count: 88,236 files at 75 per batch is 1,177 batches. At roughly
  200 batches per run (the `max_batches_per_run` default), about 6 runs complete
  the archive, assuming no OCR-heavy slowdown. OCR-heavy years (1991-2008 scans)
  will take more runs; the chain continues until `remaining_count` is 0.

## 6. Index design

Indexes are the centerpiece: an agent must resolve any document in milliseconds
without parsing a PDF.

- `llms.txt`: concise entry map (categories, years, manifest links, lookup rules).
- `llms-full.txt`: exhaustive link map (every category, every year 1991-2026).
- `INDEX.md`: master table of contents with per-category counts.
- `index/by_year/<YYYY>.md`: one Markdown index per year (1991-2026).
- `index/by_category/<Category>.md`: one Markdown index per category.
- `data/<Category>/<Year>/INDEX.md`: annual index inside every year directory,
  built by the indexer as conversion fills that year.
- `manifest/catalog/<YYYY>.jsonl`: one JSON object per document, one shard per
  year (all 92,100 census rows; DOWNLOADED rows carry `md_path` and `status`,
  BLOCKED rows carry the reason and empty PDF fields). This is the filterable
  catalog. Sharded because the single file passed GitHub's 100 MB push limit
  at 60,647 rows (103.40 MB) and killed run 43443272509 (Defect 7).
- `manifest/sha256_conversion_ledger.csv`: the conversion ground truth. One row
  per PDF: pdf_sha256, file_path, md_path, md_sha256, page counts, engine, status
  (PENDING / DONE / FAILED), converted_at_utc.
- `manifest/hf_88236_inventory.jsonl`: the 88,236-file inventory synced from
  Hugging Face (clean keys: category, year, listing_date, headline, document_id,
  listing_url, pdf_url, file_path, file_name, bytes, sha256).
- `manifest/pdf_final_direct_urls.txt`: the canonical 81,828 direct RBI PDF URLs.
- `index/url_to_path_map.json`: O(1) lookup. Keys are every RBI direct URL
  (81,828 unique) and every Hugging Face resolve URL (88,236); values are the
  `data/.../*.md` path. Total 170,064 keys. 5,951 RBI URLs map to more than one
  document (same PDF listed twice); the map holds the first path in sorted order
  and `index/url_collisions.json` holds every path for those URLs.
- `STATE.json`: the deterministic checkpoint (`total_count`, `done_count`,
  `remaining_count`, `done_paths`, `last_batch`, `updated_at_utc`, `pct`).

All index files are rebuilt deterministically from the ledger and the inventory,
sorted, so a rebuild with no new conversions produces no diff.

## 7. Weekly sync design

Workflow `02_weekly_rbi_hf_github_sync.yml` (Mondays 02:30 UTC):

- Phase A (discover): `python3 -m src.rbi_pipeline.rbi_crawler --urls
  manifest/pdf_final_direct_urls.txt --ledger
  manifest/sha256_conversion_ledger.csv --out .cache/sync/new_documents.json`
  crawls the live RBI index endpoints (Master Directions, Notifications,
  Master Circulars, Drafts, Circular Index, Press Releases) and reconciles
  against the direct-URL list and the ledger.
- Phase B (register): `scripts/register_new_documents.py` downloads each
  new PDF once, derives its canonical name (date from page 1, headline
  from page 1, category from the crawler), and appends it to the inventory
  JSONL, the ledger (PENDING), and the direct-URL list. When `HF_TOKEN`
  is configured it also backfills the PDF to the Hugging Face dataset;
  when it is not, it logs a warning and continues with RBI-direct
  conversion. Idempotent: re-running skips URLs already registered.
- Phase C (convert): the normal runner pass converts the newly registered
  pending rows from the inventory (no separate sync mode; new documents
  join the same inventory/ledger/STATE system, so STATE total grows from
  88,236 by the number of new documents), committing per batch and
  rebuilding the indexes at the end.
- Phase D (commit): the workflow commits what the runner did not stage
  (the inventory, the URL list, `sync/registered.json`) as one commit:
  `chore(sync): <n> new RBI documents -> MD | <YYYY-MM-DD> | imsovikde verified`.
  A week with zero new documents commits nothing.
- The direct RBI crawl runs even when Hugging Face reports zero new files, so a
  file HF missed is still caught here (zero-miss guarantee).
- Known limits of the sync naming: the headline comes from the PDF's page 1
  (the crawler does not record the listing page), and a new press release's
  document ID is the PDF file stem rather than the numeric listing ID. The
  file is still uniquely named, converted, and indexed; both values are
  recorded in `sync/registered.json` with their source for later correction.

## 8. Failure modes and retries

| Failure | Response |
| --- | --- |
| HF 429 / 5xx while streaming a PDF | Exponential backoff + jitter, up to 5 tries; file stays PENDING for the next batch |
| Runner killed by GitHub at 6 hours | STATE.json already committed per batch; the watchdog or the next self-chained run resumes |
| Push rejected (remote moved) | `git pull --rebase origin main`, retry push up to 3 times |
| Corrupt 1990s PDF (bad xref) | Ghostscript repair into a temp buffer; original pdf_sha256 still recorded |
| anydoc raises NeedsOcr | Hybrid OCR path (OCRmyPDF + RapidOCR/Tesseract, then PaddleOCR PP-OCRv5) |
| OCR package missing on runner | Converter falls back to anydoc-only; affected pages stay NEEDS_OCR and are retried later; ledger records the missing engine |
| Verification fails on a file | Ledger row marked FAILED with the error; file stays pending and is retried next batch; 3 consecutive all-failed batches stop the run (exit 2, no self-chain) |
| Audit finds a mismatch | AUDIT.md records it, the audit workflow fails visibly, no .md file is touched by the audit |
| PAT expires (90 days) | Pushes start failing with 401; rotate the PAT and update the GH_PAT secret; in-flight work is safe in STATE.json |
| GPG key expires (2028-11-12) | Generate a successor key, add its public half to GitHub, rotate GPG_PRIVATE_KEY/GPG_PASSPHRASE; re-signing is per-commit, so old commits stay Verified |

## 9. Deliberate deviations from the original directive (with reasons)

### Deviation A: GPG signing instead of SSH signing

The directive asked for SSH signing (`gpg.format = ssh`). This repository
already has a proven, working OpenPGP setup: a dedicated RSA 4096 GPG key
(E3A0ABB6FBEC5840), the public key registered on GitHub, three secrets
(`GH_PAT`, `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`), and four commits already
Verified by that key (run 43377069291, latest commit e0533340). Replacing a
proven setup with an untested SSH signing key would risk the one property the
whole pipeline depends on (every commit Verified). SSH signing was therefore
explicitly replaced by OpenPGP (GPG) signing. The commit identity mandate is
unchanged: every commit is authored by Souvik Dey <imsovikde@gmail.com> and
signed so GitHub shows Verified. If the owner later prefers SSH signing, the
only change is the signing step (import an SSH key, set `gpg.format ssh`);
nothing else in the pipeline depends on the signature mechanism.

### Deviation B: Hugging Face folder names preserved under data/

The directive's tree used renamed folders (`01_Master_Directions`,
`02_Notifications_1991_2026`, ...). This build preserves the Hugging Face
folder names exactly under `data/`: `Master-Directions`, `Notifications`,
`Master-Circulars`, `Draft-Notifications-Guidelines`, `Circulars`,
`Press-Releases`. Reason: the 1:1 parity invariant wins. A file's Markdown
path is derivable from its Hugging Face path by a mechanical rule
(`data/` + HF path, `.pdf` to `.md`), with no rename table to maintain and no
chance of a rename drifting between the two repositories. Numbered labels live
only in index files and documentation, never in paths. Note also that the
manifest CSV's short category labels (`Master-Direction`, `Notification`,
`Circular`, `Draft-Notification`, `Master-Circular`, `Press-Release`) are
mapped to these folder names in every generated index; the mapping is 1:1 and
lives in the indexer's category map (`src/rbi_pipeline/indexer.py`).

## 10. Security notes

- Secret values never appear in any file in this repository. Secrets live only
  in GitHub Actions secrets (`GH_PAT`, `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`,
  and later `HF_TOKEN`). The setup script refuses to print them.
- The GPG private key is imported only inside the runner (ephemeral, destroyed
  with the runner) via `crazy-max/ghaction-import-gpg@v6`.
- `.gitignore` blocks key material, tokens, `.env` files, and `*_secret*` files.
- The PAT is fine-grained, scoped to this repository only, Contents read/write,
  90-day expiry. It cannot touch workflows or dispatch runs, which is why
  workflow files are landed via the web UI and self-chaining uses `GITHUB_TOKEN`.

## 11. Integration fixes found by the local smoke test (13 Nov 2026)

A full end-to-end run of the runner against 3 real PDFs (downloaded from the
public Hugging Face dataset, converted, committed with a test GPG key) caught
four bugs before launch. Each is fixed in the code in this bundle:

1. **Ledger upsert, not append.** The runner appended one row per conversion,
   so a converted file had two rows (PENDING seed + DONE). The audit's
   row-count check and the catalog would then disagree with STATE.json.
   `upsert_ledger_rows` now replaces the file's PENDING row in place, so the
   ledger stays exactly one row per file. The seed ledger was regenerated to
   the runner's 20-column format to match.
2. **Index rebuild must be committed.** The graceful-stop index rebuild
   rewrites tracked files (INDEX.md, README.md, llms.txt, the URL map, the
   catalog). Left uncommitted, the next run's `git pull --rebase` fails on
   unstaged changes and the pipeline stalls. The runner now commits the
   rebuild as its own signed commit (`chore(index): rebuild indexes | ...`),
   and recovers an uncommitted rebuild at the next startup. README.md is
   part of the index commit set.
3. **All-failed batches must stop the run.** A batch in which every download
   fails was retried forever (same pending files, empty commits) until the
   time budget expired. Three consecutive zero-conversion batches now stop
   the run with exit code 2, and the workflow only self-chains after a
   successful run, so a systemic failure cannot chain into a failure storm.
   The 6-hour watchdog cron retries later.
4. **Proxy-safe HTTP client.** `httpx` with default settings fails on
   environments whose NO_PROXY list contains bracketed IPv6 entries
   (`[::1]`) with `InvalidURL: Invalid port`, and with `trust_env=False` it
   drops `SSL_CERT_FILE` (the egress proxy's CA bundle) and fails TLS
   verification. `hf_enumerator._http_client` passes the proxy explicitly,
   disables `trust_env`, and passes `SSL_CERT_FILE` as the verify bundle,
   so downloads work both behind this VM's egress proxy and on plain
   GitHub Actions runners (no proxy variables set there). Verification is
   never disabled. The same helper is used by the RBI crawler.
5. **Pilot brake.** The bootstrap dispatches workflow 01 with
   `max_batches_per_run=2` and `self_chain=false`, so the first 150 files
   are verified by a human before the full run is dispatched by hand.
   Workflow 01 also accepts a `self_chain` input (default true).
