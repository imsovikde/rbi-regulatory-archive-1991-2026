# CONTEXT TRANSFER — RBI Regulatory Archive: PDF-to-Markdown Conversion Engine

## How to use this file

You are the receiving agent. This file is your entire briefing. Read it top to bottom, then act. Do not ask the user for anything this file already answers. Do not come back until the engine described here is running end to end and verified. The user will paste this file to you as the prompt. That paste is your full authorisation to do the work below.

First action after reading: clone the repository named in Section 1, then commit this file into it at `docs/CONTEXT-TRANSFER.md` (one commit, message `docs: add living context transfer file`, authored by Souvik Dey, GPG-signed, Verified — see Section 6). The repository must carry its own context from then on. Then check the live repository state against Section 3. Where live GitHub state disagrees with this file, live state wins for counts and you must update this file to match.

Last updated: 14 November 2026, 01:24 IST. Every later change to the facts in this file must update this line and the dated state block in Section 3. See Section 17 for the living-document protocol.

---

## 0. Operating orders (the mandate)

1. **Do not return until done.** Build, fix, launch, and verify the complete autonomous engine. A skeleton is not done. A workflow that has never run green end to end is not done.
2. **Verify, then assert.** Never state a count, date, ID, hash, or status you have not checked against a live source in this session. A claim verified nowhere is not written anywhere.
3. **Commit identity is absolute.** Every commit the pipeline makes is authored by Souvik Dey `<imsovikde@gmail.com>` and cryptographically signed with his personal GPG key, showing the green Verified badge. Bot commits and unsigned commits are strictly forbidden. The only exception is a commit made through the GitHub web UI, which is signed by GitHub's web-flow key and also shows Verified. Disclose that distinction in the final report.
4. **No PDF is ever invented.** If the RBI has no PDF for an entry, it is recorded BLOCKED with evidence. Never fabricate, reconstruct, OCR-invent, or substitute a document.
5. **PDFs are immutable.** Exact bytes as served by the RBI or Hugging Face. The only permitted change is the external file name. Never edit, re-save, OCR, or compress a PDF.
6. **Report only verified counts, with the delta stated.** Never claim completion until the gates in Section 15 prove it. Progress totals are stated as progress, never as completion.
7. **The "do not stop until 100%" condition is not accepted as a binding contract as written.** Work proceeds census-first: discovered against downloaded against verified against uploaded, with the remaining delta reported at every step. Full 100% conversion is a function of runner time; the deliverable of this session is the complete engine launched and verified end to end on pilot batches with the self-chaining loop running, plus a measured throughput and an ETA estimate. Do not claim 100% until STATE.json and the ledger prove it.
8. **Own every mistake in the same turn it is found.** Fix it, disclose exactly what changed, and prove fidelity with verifiable diffs, counts, or hashes.
9. **Never ask for a secret in chat.** Secrets are named in Section 5. Their values are write-only on GitHub and were never recorded anywhere. Never log a token, a passphrase, a private key, or a presigned URL.
10. **Keep the two archive runs strictly separate.** Never read, list, copy, link to, or reuse anything from the other agent's run (Section 13). Nothing is merged, closed, or duplicated without the user saying so first.

---

## 1. Identity and accounts

- **User:** Rohit. Legal name Souvik Dey, used only on filings and case records. In conversation, call him Rohit. English only, unless he explicitly asks for another language.
- **GitHub:** login `imsovikde`, user id `153044727`, email `imsovikde@gmail.com`, display name Souvik Dey.
- **Hugging Face:** user `imsovikde`, user id `683f0896ce4e861c3275576c`, full name Souvik Dey.
- **Timezone:** Asia/Kolkata (IST, UTC+5:30). All times in this file are IST unless marked UTC.
- **GitHub sign-in has two-factor authentication via authenticator app (TOTP).** Codes are NOT emailed. Any browser sign-in stalls at 2FA until the user supplies the current 6-digit code from his authenticator app, approves in GitHub Mobile, or enters a recovery code. Do not look for a GitHub code in email; none will arrive.
- **GitHub fine-grained token `TEMP_CLAUDE` expired around 10 November 2026.** Do not reuse it.

---

## 2. Mission and scope

Convert every PDF in the RBI Regulatory Archive (1991–2026) into GitHub-ready Markdown, in the same repository that indexes the archive, with full automation afterwards.

- **Source of PDFs:** the public Hugging Face dataset `imsovikde/rbi-regulatory-archive-1991-2026` (Section 11). The RBI site is the fallback source only (Section 12).
- **Destination:** the public GitHub repository `imsovikde/rbi-regulatory-archive-1991-2026` (Section 3). Markdown files live under `data/` in that repo, mirroring the Hugging Face folder structure exactly.
- **Total scope: 88,236 PDFs.** Per-category counts are in Section 7.
- **What "done" means:** Section 15. In short: 88,236 Markdown files, every one with valid frontmatter, SHA fields, and page parity; all indexes 100% populated; workflows 01, 02, and 03 active and passing; every commit on `main` Verified under imsovikde.
- **What is NOT in scope:** the other agent's parallel archive run (never touch it); Google Drive (the Drive copy of this run was deleted by the user on 11 November 2026 because the file size was too large — do not restore it to Drive unless the user explicitly orders it); the Cloudflare query layer (designed, not built); the Internet Archive mirror (not created); a Hugging Face Space search UI (not built).
- **Original authority:** the user's Ultimate Prompt of 11 November 2026 is primary. A second, lower-precedence prompt exists; its baseline counts are unverified hypotheses, never targets. Where the pasted directive and this file disagree, this file wins, because it records what was actually built and verified.

---

## 3. Current verified state (14 November 2026, 01:24 IST)

Update this block in place whenever a fact below changes. Keep the old value struck through with its date; never silently overwrite history.

### 3.1 Hugging Face dataset (PDFs — COMPLETE and verified)

- Dataset: `imsovikde/rbi-regulatory-archive-1991-2026`, public, id `6af59bc904804d7cc2eb5604`.
- URL: https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026
- **PDFs on Hugging Face: 88,236. Verified 13 November 2026 09:07 IST: local 88,236 / remote 88,236, 0 missing, 0 extra, 0 SHA-256 mismatch, spot re-hash 120/120.**
- Commits on the dataset: 460 at the retry verification (head `78c006f0bd69453bd9fae3d8adb7998a6da5276c`), then two more: data card README (`6a5364b7`) and viewer manifest (`f2342995`). Current head: `f23429951c145ad3fd35160b4be10e5f14421ded`. Siblings: 88,239 (88,236 PDFs + README.md + data/manifest.csv + .gitattributes). PDF count unchanged by those two commits.
- `usedStorage` after retry: 15,401,583,594 bytes. After README + manifest: 15,453,812,792 bytes.
- **Manifest: 92,100 rows** (`SHA256_MANIFEST.csv`, `INVENTORY.csv`, `sha256_master_ledger.csv`). DOWNLOADED 88,236, BLOCKED 3,864.
- Inventory frozen 11 November 2026 ~00:18 IST. Expected count 92,085. Downloaded 88,220, blocked 3,865, failed 0 in the original run. Retry run 13 November 2026 09:07 IST re-checked all 3,865 blocked entries: recovered 2 (Notification 1492, dated 2004-01-24, 606,753 bytes, merged; Notification 287, dated 1989-03-25, out of scope pre-1991, kept aside, NOT merged, NOT on Hugging Face). Still blocked: 3,863. Post-freeze additions merged: 15 (Master Direction 13752, 11 November 2026, MD + Notification copies, byte-identical; Press Releases 63953–63965). MD 12896 re-issued by the RBI (451,160 → 446,662 bytes, SHA starting `325b612e`); both copies replaced, stale copy deleted from Hugging Face (commit `78c006f0`).
- Blocked breakdown: 61 dateless-downloadable (preserved as evidence only, 85 files / 14.75 MB, NOT merged), 28 HTTP 418 bot-wall, 27 HTTP 404, 8 RBI error-page, 6 zero-byte, 18 no PDF link, 3,715 zero new links. Detail in `_manifests/unavailable_pdf_entries.csv`, `_manifests/bot_blocked_urls.json`, `_manifests/dead_links.json`, `_manifests/retry_state.jsonl`.
- Local tree (recovery store, intact): `~/workspace/rbi-archive-muse/`, 88,236 PDFs, 21.85 GB excluding `.cache/`. Original exact PDF byte total for 88,220 files: 21,182,477,977 bytes (21.18 GB decimal / 19.73 GiB). Largest single PDF: 8,033,755 bytes. Zero files over 50 MB. Whole staging is 36 GB including a 16 GB `.cache/`.
- **Parquet viewer:** the dataset's Discussion #1 is the official Hugging Face parquet-converter bot, NOT a person. Hugging Face has no product called "Data Studio"; the Dataset Viewer is the equivalent. The viewer table was NOT yet confirmed live when last checked (~10:20 IST 13 November 2026): the `refs/convert/parquet` branch was temporarily 404 and `/api/datasets/{repo}/parquet` returned 400 "server busier than usual". Re-check it. A reply was posted to Discussion #1 as imsovikde (comment id `6af694b0d771af56e7aa437f`, verified visible). A test probe comment (`6af694b883e6f87e9bfe033d`, "test probe - please ignore") was posted while finding the correct endpoint and hidden immediately.

### 3.2 GitHub repository (Markdown index — LIVE, AUTONOMOUS CONVERSION IN PROGRESS)

- Repository: `imsovikde/rbi-regulatory-archive-1991-2026`, public, id `1456135028`, default branch `main`.
- URL: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026
- **Markdown files converted so far: ~~0 / 88,236~~ → ~~4,575 / 88,236 (5.1850%), 13 Nov 2026 14:46 IST~~ → ~~16,500 / 88,236 (18.6999%), 13 Nov 2026 ~18:05 IST~~ → ~~17,250 / 88,236 (19.5498%), 13 Nov 2026 ~18:21 IST~~ → ~~23,775 / 88,236 (26.9448%), 13 Nov 2026 ~19:44 IST~~ → ~~23,925 / 88,236 (27.1148%), 13 Nov 2026 ~19:47 IST~~ → ~~24,375 / 88,236 (27.6248%), 13 Nov 2026 ~20:07 IST~~ → ~~47,100 / 88,236 (53.3796%), 13 Nov 2026 23:17 IST~~ → ~~60,647 / 88,236 (68.7327%), 14 Nov 2026 00:42 IST~~ → ~~61,022 / 88,236 (69.1577%), 14 Nov 2026 01:12 IST~~ → 61,172 / 88,236 (69.3277%), 14 Nov 2026 01:23 IST.** Verified from commits: batch `61,172` Press-Releases. Per category: Master-Directions 397/397, Notifications 10,527/10,527, Master-Circulars 1,013/1,013, Draft-Notifications-Guidelines 546/546, Circulars 11,690/11,690, Press-Releases 36,999/64,063. Only Press-Releases remains.)
- Commits on `main` (newest first, all authored AND committed by Souvik Dey, all Verified):
  - `b2a9380` — "fix(workflows): checkout latest main so queued runs never go stale" — 13 Nov 2026 18:12 IST. Authored by imsovikde, committer GitHub (web-flow signature, Verified). 3 files, 27 additions, 0 deletions. Fixed Defect 4 (Section 4).
  - `8e18bf3` — "chore(index): rebuild indexes | 16500/88236 PDFs -> MD" — 13 Nov 2026 ~18:05 IST. GPG-signed, Verified. Conversion reached 16,500/88,236 (18.6999%) via chained runs after pilot run #2.
  - `91a9c12` — batch #220, Notifications/2007, 75 anydoc + 0 OCR. `cc4d662` #219, `d2cbc3c` #218 (70 anydoc + 5 OCR). All GPG-signed, Verified.
  - `05f733b` — "fix(audit): support CRLF normalization and NT extended paths in integrity audit" — 13 Nov 2026 13:58 IST. GPG-signed, Verified.
  - `0c4f181` ... `83856ed` ... `c31fa6c` — 45 batch commits (Batch #1 through #45) converting Circulars 1992–2009. All GPG-signed by runner, Verified.
  - `befaecb` — "fix(workflows): add actions:write permission and remove missing pip cache" — 13 Nov 2026 13:07 IST. Fixed Defect 1 & Defect 2. GPG-signed, Verified.
  - `8e715a1` — "docs: add living context transfer file" — 13 Nov 2026 12:55 IST. GPG-signed, Verified.
  - `a690935` — "feat: land RBI Markdown conversion pipeline (bootstrap)" — 13 November 2026 12:34 IST. The pipeline bundle, landed by bootstrap run #1. GPG-signed, Verified.
  - `fd078a6` — "Add RBI Markdown conversion workflows (00 bootstrap, 01 conversion, 02 weekly sync, 03 audit)" — 13 November 2026 12:32 IST. 4 files, 474 additions. Authored by imsovikde, committer GitHub (web-flow signature, Verified). Landed via the GitHub web UI.
  - `4573a7d` — "Record verified Actions signing proof in setup report".
  - `e053334` — "chore: archive update 2026-11-13".
  - `e868454` — "Add GPG setup report and secret-safe gitignore".
  - `abced89b`, `96291352` — earlier GPG setup commits.
- **Pilot run #2 (Run 43387158709): SUCCESS / IN PROGRESS.** Dispatched 13 Nov 2026 13:08 IST. Steps 1–5 passed green in ~1 minute. Conversion loop actively executing; converted 3,375 files across 45 batches with zero failures in first 50 minutes. Chained runs then carried conversion to 16,500/88,236 (18.6999%) by ~18:05 IST (16,500 − 4,575 = 11,925 = 159 batches × 75).
- **Run 43394196880 (workflow 01): FAILED.** Dispatched 13 Nov 2026 14:03 IST, head `dbe5544`; queued ~3h46m behind the concurrency group; job ran 17:50–17:52 IST and failed in 6 seconds at step 7 (startup index-recovery commit rebase conflict). Cause: see Section 4, Defect 4 (RESOLVED).
- **Run 43427571590 (workflow 01): FAILED at batch #320.** Dispatched 13 Nov 2026 18:13 IST on commit `b2a9380`, defaults. Converted batches #221–#319 (16,500 → 23,925/88,236, 27.1148%), then failed at 19:46:39 IST at batch #320 with a push rejection. Cause: see Section 4, Defect 6 (RESOLVED). Self-chain skipped; the pipeline stopped until run 43443272509 was dispatched by hand.
- **Run 43443272509 (workflow 01): FAILED at batch #809.** Dispatched 13 Nov 2026 20:00 IST on commit `02bd3b5` (the Defect 6 fix), defaults. Converted batches #320–#809 (23,925 → 60,647/88,236, 68.7327%), then failed at ~00:52 IST at the graceful stop: the index commit was rejected because `manifest/master_catalog.jsonl` was 103.40 MB, over GitHub's 100 MB limit. Cause: see Section 4, Defect 7 (RESOLVED). Self-chain skipped (convert step exit 2); the pipeline stopped until run #7 was dispatched by hand.
- **Run 43493887762 (workflow 01, run #6): FAILED in 6m 1s.** Scheduled (watchdog cron, fired late at 01:06 IST on 14 Nov), head `f28bec9` (old code, before the Defect 7 fix). It converted batches to 61,022/88,236 (69.1577%), then failed; most likely cause is the Defect 7 fix landing (three commits 01:10–01:13 IST) moving main underneath its startup recovery commit (Defect 4 pattern). Not proven from its log; the batch work is safe on main.
- **Run 43495619184 (workflow 01, run #7): RUNNING, RESUME VERIFIED.** Dispatched 14 Nov 2026 01:18 IST on commit `cc6f16f` (the Defect 7 fix), defaults (batch_size 75, max_batches_per_run 200, self_chain true). Resume proven: startup recovery index commit landed, then batches past 61,022, reaching 61,172/88,236 (69.3277%) by 01:23 IST. Run status confirmed via the authenticated GitHub API (in_progress, head `cc6f16f`). Full proof of the Defect 7 fix still needs this run's graceful stop: its index commit must succeed and the self-chain must fire.
- **Bootstrap run #1: FAILED.** Run 43383089432, https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/actions/runs/43383089432, 13 November 2026 12:34–12:35 IST. Steps 1–5 passed (checkout, GPG signing setup, bundle download from Hugging Face, bundle commit as Verified). Step 6, "Dispatch Continuous Conversion Workflow (pilot: 2 batches, no self-chain)", FAILED. Cause: see Section 4, Defect 1 (RESOLVED).
- **Pilot run #1: FAILED.** Run 43383873884, https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/actions/runs/43383873884, 13 November 2026 12:40–12:41 IST. Failed at step 5 (missing pip cache). Cause: see Section 4, Defect 2 (RESOLVED).
- **Job logs cannot be downloaded through the unauthenticated GitHub API** (403 "Must have admin rights to Repository"). Read a failing step's log through the browser while signed in as the user, or through an authenticated API call.
- **Unauthenticated GitHub API is rate-limited to 60 requests/hour on the shared egress IP** and that budget is shared with other traffic; it was exhausted once during diagnosis. Prefer authenticated access or the web UI for reads.

### 3.3 What is already built and where it lives

- Pipeline source of truth: `~/workspace/rbi-archive-muse/pipeline-build/` — `src/rbi_pipeline/` (8 Python modules), `repo/` (the bundle that was landed), `MANIFEST.txt` (73 paths), `TEST-REPORT.md`, `smoke/` (test rig), `venv/` (538 MB test venv with PyMuPDF, anydoc 0.2.4, rapidocr-onnxruntime 1.4.4).
- Bundle on Hugging Face: `_pipeline/bootstrap/` (74 files including MANIFEST.txt itself), MANIFEST.txt md5 `fa23fe46d2888f34c5f01aa3555fff45`, verified identical local/remote. Upload commits `9fd9546c` + `f8cba21e` (first), `9f72c862` (after fixes).
- Reports: `~/workspace/rbi-archive-muse/_manifests/FINAL_REPORT.md` (original download run), `~/workspace/rbi-archive-muse/_manifests/RETRY-REPORT-2026-11-13.md` (retry run), `~/workspace/rbi-archive-muse/_manifests/pdf_source_endpoints.md` and `~/workspace/rbi-archive-muse/_manifests/pdf_final_direct_urls.txt` (81,828 unique URLs).
- The local scaffold at `~/workspace/rbi-archive-muse/github-ready/repo/` is STALE (counts say 88,220, pre-retry report). Do NOT push it as-is. Refresh to 88,236 and reconcile with the repo's existing files first, or ignore it entirely; the live bundle is `pipeline-build/repo/`.

---

## 4. Blocking defects — fix these first

Two defects block the engine. Both are in the workflow files that are already on `main`. Fix them, re-land the files, re-run the pilot. Nothing else in the pipeline is known-broken.

### Defect 1 — Workflows cannot dispatch other workflows (breaks bootstrap step 6 and 01 self-chaining)

- **Fact:** all four workflow files declare only `permissions: contents: write`. Dispatching a workflow through the API (`gh workflow run`, which calls the workflow-dispatch endpoint) requires `actions: write`. The `GITHUB_TOKEN` in a run therefore cannot fire the next run. This is why bootstrap run #1 failed at step 6, and it is also why workflow 01's self-chain step would fail the same way when the full run tries to chain.
- **Fix:** in `00_bootstrap.yml` and `01_continuous_conversion.yml`, change the permissions block to:
  ```yaml
  permissions:
    contents: write
    actions: write
  ```
- `02_weekly_rbi_hf_github_sync.yml` and `03_integrity_audit.yml` do not dispatch anything. Leave their permissions unchanged.
- **Why not the PAT:** the fine-grained PAT `GH_PAT` has Contents read/write only and cannot dispatch workflows either. `GITHUB_TOKEN` is the correct token for dispatch, but only once the workflow declares `actions: write`. (A workflow run triggered by `GITHUB_TOKEN` can dispatch `workflow_dispatch` events; the restriction is that other event types triggered by `GITHUB_TOKEN` do not start new runs.)

### Defect 2 — Python setup fails: pip cache enabled, no dependency file (breaks 01 pilot and 02 weekly sync)

- **Fact:** `01_continuous_conversion.yml` and `02_weekly_rbi_hf_github_sync.yml` use `actions/setup-python@v5` with `cache: "pip"`. The repository contains no `requirements.txt`, no `pyproject.toml`, and no `setup.py`, so the cache lookup matches nothing and the step errors. Pilot run #1 died on this step in 27 seconds. Workflow 02 has the identical bug and would fail on its first Monday run. Workflow 03 uses setup-python WITHOUT a cache line and is clean. Workflow 00 has no Python step.
- **Fix:** in `01_continuous_conversion.yml` and `02_weekly_rbi_hf_github_sync.yml`, delete the `cache: "pip"` line from the setup-python step. Keep `python-version: "3.11"`. The install step that follows installs the stack explicitly, so nothing is lost; each run simply reinstalls (a few minutes against a 6-hour run).
- Do NOT "fix" this by inventing a requirements file that duplicates the install step unless the user asks for it.

### How to land fixed workflow files (read this before touching them)

- **The PAT cannot push workflow files.** `GH_PAT` is a fine-grained PAT with Contents read/write only and no Workflows scope. Any push that touches `.github/workflows/` is rejected by GitHub. The bootstrap workflow itself must never write into `.github/workflows/` either.
- **Land workflow files through the GitHub web UI** ("Add file" → "Upload files", exact filenames, byte-for-byte), in ONE commit, direct to `main`. Web-UI commits are authored by imsovikde and show Verified (GitHub web-flow signature). That is the disclosed exception to the GPG rule in Section 0.
- **Alternative:** `gh` authenticated as the user, or the GitHub web editor. Never use the PAT, never use `GITHUB_TOKEN` from a workflow run, never force-push.
- **After landing:** verify each landed file byte-for-byte. Fetch the raw file from `main` and compare SHA-256 against your local copy. Pre-fix SHA-256 values (for reference only — they change when you edit):
  - `00_bootstrap.yml`: `0da81baf6dcf32908c147c476e1ce923a837b3141a6c5bb2a3de9c67959b40f4`
  - `01_continuous_conversion.yml`: `24153bf510c2dd09d92100a89b267257e9239ea3a5e06d9e59e52ac22a73df06`
  - `02_weekly_rbi_hf_github_sync.yml`: `fbe5edc9f53e64e6483285aa14379faae8506924ab538b15ed0b7c2535bc81be`
  - `03_integrity_audit.yml`: `2ca6412398c95a056f3534109db2b5634a145159f0160ce0fec20deee2276531`
- **Post-fix Git blob SHA-256 values (landed in commit `befaecb`, 13 Nov 2026):**
  - `00_bootstrap.yml`: `c04e0c77e634853faf9b281035f421af39ec6c1f93abc5fde582ac53fdd0f3c7`
  - `01_continuous_conversion.yml`: `653f706e5fe6c79a135c1ca81174de2b0b47c08edbdeb026b31d73a285dfe480`
  - `02_weekly_rbi_hf_github_sync.yml`: `bfa8d69c32e94ad20cc38d27cc29c25989b221da1f2af242f6088afb83cf97d1`
  - `03_integrity_audit.yml`: `00ae657614b4942fc85d7254a859831e1d01ebd7519b392ebf8e85ac2e7c2707`

### Defect 3 — `audit_parity.py` failed check (a) on CRLF checkouts and Win32 MAX_PATH (RESOLVED)

- **Fact:** `split_frontmatter` had hardcoded `if not text.startswith("---\n"):`, which broke when files were checked out on Windows where line endings are CRLF (`\r\n`). In addition, 129 legacy Circular files have filenames exceeding Windows MAX_PATH (260 characters), causing standard `os.path.exists` on Windows to fail unless prefixed with `\\?\`.
- **Fix (commit `05f733b`, 13 Nov 2026):** in `scripts/audit_parity.py`, normalized `text = text.replace("\r\n", "\n")` in `split_frontmatter`, and added `if os.name == "nt" and not md_path.startswith("\\\\?\\"): md_path = "\\\\?\\" + os.path.abspath(md_path)` in `check_a()`.
- **Verification:** `python scripts/audit_parity.py` returned exit code 0 (`4/4 checks passed (PASS); 2253/2253 items verified`).
- **Then re-run:** dispatch workflow 00 (bootstrap) again by hand, OR dispatch workflow 01 directly as the pilot (batch_size 75, max_batches_per_run 2, self_chain false). Either path is correct; the pilot is what must be verified. If the bootstrap dispatch still fails after the fix, read the failing step's log in the browser and report the exact error text before trying anything else.

### Defect 4 — Queued run checks out a stale commit; startup index-recovery commit fails to rebase (RESOLVED)

- **Fact:** Run 43394196880 (workflow 01, dispatched 13 Nov 2026 14:03 IST) sat queued ~3h46m behind the concurrency group `rbi-markdown-conversion-pipeline` while the previous chained run kept committing. When its job finally started at 17:50 IST, checkout (no `ref:` specified) checked out the dispatch-time head `dbe5544`, 159 commits behind main. The runner's startup index-recovery commit `0bd87d39` ("chore(index): rebuild indexes (recovered from previous run)") was built from that stale state, and `git pull --rebase origin main` (fetching `dbe55443..8e18bf3b`) conflicted applying it. Step 7 failed in 6 seconds, exit code 2; step 8 (self-chain) skipped; the pipeline stopped at 16,500/88,236 (18.6999%). Earlier runs worked because they started promptly with a fresh head. Same code, different timing.
- **Evidence:** Step 7 log (28 lines, read in the browser as imsovikde, 13 Nov 2026 18:09 IST): line 19 `fatal: index recovery commit failed: git pull --rebase origin main failed (exit 1)`; line 23 `error: could not apply 0bd87d39... chore(index): rebuild indexes (recovered from previous run)`. No Python traceback, no GPG/403/404/429/disk error.
- **Fix (commit `b2a9380`, 13 Nov 2026 18:12 IST):** added `ref: main` to the checkout step (`actions/checkout@v4`, `with: token: ${{ secrets.GH_PAT }}`) in `00_bootstrap.yml`, `01_continuous_conversion.yml`, `02_weekly_rbi_hf_github_sync.yml`. Every run now checks out the tip of main when its job starts, so a queued run can never go stale. Nothing else changed: diff proves 9 added lines per file (comment + `ref: main`), 27 additions, 0 deletions; all three files parse as valid YAML. Converter, batching, signing, batch commit format (anydoc + OCR counts, [XX.XXXX%]) untouched. The runner itself was NOT changed (deliberate: avoid new-bug risk; the checkout fix removes the stale-head trigger at its root). Landed via the GitHub web UI in one commit, authored by imsovikde, committer GitHub (web-flow signature, Verified). Landed files verified byte-identical to the edited files by SHA-256 (00 `228b2f8b...`, 01 `1f97df52...`, 02 `d3dfe91c...`).
- **Verification (PASSED 13 Nov 2026 ~18:21 IST):** run 43427571590, dispatched 18:13 IST on commit `b2a9380`, got past startup and converted batches #221–#230, reaching 17,250/88,236 (19.5498%) — latest commit `f4d34e1` "[19.5498%] 17250/88236 PDFs -> MD | Notifications/2009 Batch #230 | 69 anydoc + 6 OCR verified". Run in progress. Self-chain at the time limit remains to be observed; the mechanism was proven by the earlier chained runs. (That run later failed at batch #320 — see Defect 6.)

### Defect 5 — Workflows 00/01/02 used separate concurrency groups; concurrent pushes to main could collide (PREVENTIVE FIX)

- **Fact:** 00, 01 and 02 each had their own concurrency group (`rbi-bootstrap-pipeline`, `rbi-markdown-conversion-pipeline`, `rbi-weekly-sync-pipeline`). 02 runs the normal runner and pushes batch commits; 00 commits the bundle and pushes; both can run while a 01 run is active, and their pushes (`git pull --rebase` + push on the same files: ledger, STATE.json, manifest, indexes) can collide the same way Defect 4 did. Not yet observed failing: no 02 run has overlapped a 01 run since the pipeline started (02 first runs Monday 17 Nov 2026 02:30 UTC; 00 already ran once successfully). Found by a full failure-mode audit on 13 Nov 2026 19:44 IST, ordered by the user after Defect 4.
- **Evidence:** live workflow files read 13 Nov 2026 19:45 IST: 00 group `rbi-bootstrap-pipeline`, 01 group `rbi-markdown-conversion-pipeline`, 02 group `rbi-weekly-sync-pipeline`. 02 runs `python3 -m src.rbi_pipeline.runner`. 00 dispatches 01 via `gh workflow run 01_continuous_conversion.yml`.
- **Fix (commit `4dd047d`, 13 Nov 2026 19:46 IST):** 00 and 02 now share 01's group `rbi-markdown-conversion-pipeline`. All three workflows that push to main serialize behind one group, so two of them can never push at once. 03 and `archive-update.yml` keep their own groups: they touch only `AUDIT.md` / `.archive-runs/last-run.txt`, files no other workflow touches, so they cannot conflict. Nothing else changed: diff proves only the group line plus a comment changed in each file; both files parse as valid YAML.
- **Verification:** landed files verified byte-identical by SHA-256 (00 `a557d633...`, 02 `3ed3aa91...`). The queuing behaviour itself (a 02 run waiting behind an active 01 run) is verified only when it first happens — 02's first run is Monday 17 Nov 2026 02:30 UTC. Do not mark fully verified until then; the landing itself is verified.

### Defect 6 — Push retry never re-syncs; a commit landing mid-push kills the run (RESOLVED)

- **Fact:** Run 43427571590 failed at 19:46:39 IST at batch #320 with `CommitError: git push failed after 3 attempts: git push origin HEAD:main failed (exit 1)` / `! [rejected] HEAD -> main (fetch first)`. The direct trigger was commit `4dd047d` (the Defect 5 fix) landing on main at 19:46 IST while batch #320 was pushing. The deeper cause is a bug in `src/rbi_pipeline/git_committer.py`: `commit_batch` runs `commit -S`, then `pull --rebase`, then a retry loop that retries ONLY the push. It never re-syncs between attempts, so a push rejected because main moved fails every retry with the same rejection. The retry as written could only ever help a transient network blip, never a moved main.
- **Evidence:** Step 7 log (1,627 lines, read in the browser as imsovikde, 13 Nov 2026 19:55 IST): batch #319 committed 14:16:00Z (23,925/88,236, 27.1148%); batch #320 started 14:16:00Z, converted 75 files, then traceback `runner.py` line 638 → `git_committer.py` line 153 → `CommitError`. No conversion, disk, HF or HTTP error. Code read from main confirms the retry loop contains only the push.
- **Fix (commit `02bd3b5`, 13 Nov 2026 19:58 IST):** before each retry after the first, `commit_batch` now re-runs `git pull --rebase origin main`; on a rebase conflict it aborts the rebase (`git rebase --abort`) and raises CommitError. Verified by a local race test (`test_push_retry.py`, pre-push hook pushing a second clone's commit mid-push): OLD code fails with the exact production error and loses the batch; FIXED code succeeds and main ends [seed, other commit, batch commit]. Landed via the GitHub web UI, Verified, byte-identical (SHA-256 `7872e00a...`), 18 additions, 0 deletions. Return contract unchanged (True pushed / False nothing staged / raises CommitError); the fix also covers the index-rebuild and startup-recovery commits, which use the same function.
- **Verification (PASSED 13 Nov 2026 ~20:07 IST):** run 43443272509, dispatched 20:00 IST on commit `02bd3b5`, got past startup and converted batches #320–#325, reaching 24,375/88,236 (27.6248%) — latest commit `908378c` "[27.6248%] 24375/88236 PDFs -> MD | Press-Releases/1993 Batch #325 | 64 anydoc + 11 OCR verified". Run in progress. Self-chain at the time limit remains to be observed. (That run later failed at batch #809 — see Defect 7.)

### Defect 7 — Single catalog file passed GitHub's 100 MB push limit; index commit rejected (RESOLVED)

- **Fact:** Run 43443272509 converted cleanly for 4h 41m (batches #320–#809, 23,925 → 60,647/88,236, 68.7327%), then failed at the graceful stop (~00:52 IST, 14 Nov 2026) with `fatal: index commit failed: git push failed after 3 attempts` / remote error `File manifest/master_catalog.jsonl is 103.40 MB; this exceeds GitHub's file size limit of 100.00 MB` / `GH001: Large files detected`. Exit code 2, so the self-chain step was correctly skipped and no chained run started.
- **Root cause:** `manifest/master_catalog.jsonl` holds one JSON object per inventory row (~1.7 KB per row) and grows with every converted file. It crossed 100 MB at ~58,500 done. Earlier index commits succeeded only because the file was still under the limit; batch commits never touch the catalog, so conversion kept working while the index commit was doomed. Nobody (builder, reviewer, or the other agent) had checked the catalog's size against the limit. The design had no size guard and no sharding.
- **Evidence:** Step 7 log (lines 1654–1664, read in the browser as imsovikde, 14 Nov 2026 01:04 IST): batch #809 partial commit 60,647/88,236 (68.7327%), "time budget reached; stopping with state flushed for self-chain", "indexes rebuilt: 60647/88236 done", then the push rejection naming only `manifest/master_catalog.jsonl`. No Python traceback; conversion, disk, HF and HTTP were all healthy.
- **Fix (landed 14 Nov 2026 ~01:13 IST, three Verified web-flow commits):** (1) `60977d2` deleted `manifest/master_catalog.jsonl` (88,236 deletions). (2) `7389e3a` changed `indexer.py` (`_build_master_catalog` now writes one shard per year, `manifest/catalog/<YYYY>.jsonl`, same record shape) and `runner.py` (`_index_paths` lists the shard directory, never the old file). A per-category split was rejected: Press-Releases alone would be ~109 MB. (3) `cc6f16f` updated the catalog references in README.md and ARCHITECTURE.md. Verified locally before landing: 35 shards over the full 88,236-row inventory, 88,236 rows total, largest shard 2016.jsonl 5.50 MB, record keys unchanged, no single file written; end-to-end index-commit push test passed. All four landed files verified byte-identical by SHA-256.
- **Verification (RESUME PROVEN 14 Nov 2026 01:23 IST; full handoff proof still pending):** run #7 (43495619184), dispatched 01:18 IST on `cc6f16f`, is running and converting on the fixed code — startup recovery index commit landed, batches reached 61,172/88,236 (69.3277%) by 01:23 IST, run status confirmed in_progress via the authenticated GitHub API. Full proof needs the next graceful stop: its index commit must succeed and the self-chain must fire. Until then, do not claim the handoff is proven.
- **Run #6 note:** the scheduled watchdog run 43493887762 started 01:06 IST on old code (head `f28bec9`), converted to 61,022/88,236, and failed after 6m 1s, most likely because the three fix commits landed while it was starting up (Defect 4 pattern: stale head, rebase conflict at the startup recovery commit). Not proven from its log. Two corrections to earlier claims: (a) the watchdog cron DOES fire (run #6 is proof), but late (the 23:45 IST firing started at 01:06 IST, ~81 minutes late), so it is a slow backup, not a prompt one; (b) no chained run has ever been created yet — the self-chain mechanism itself is still unproven in production.
- **Operating rule from this defect:** never let a single tracked file grow unbounded; any file the pipeline rewrites every run must stay sharded or capped well under 100 MB, and its size must be checked against the limit before each landing. The catalog, the ledger (~72 MB at completion) and `index/url_to_path_map.json` (~25 MB) are the three files to watch; the ledger and the URL map are under the limit but are the next candidates if they ever grow.
- **Operating rule from this defect:** do not push to main while a conversion run is active unless the push is required to fix the run itself. The retry fix makes a mid-run push survivable, but avoiding the race is still the rule. This defect was caused by pushing the Defect 5 fix while run 43427571590 was converting.

---

## 5. Secrets inventory (names only — values are write-only, never recorded)

All four secrets exist in the repository `imsovikde/rbi-regulatory-archive-1991-2026` under Settings → Secrets and variables → Actions. Verify presence by name only (the API list endpoint shows names, never values). Never print, log, or paste a value.

| Secret | Purpose | Status |
|---|---|---|
| `GH_PAT` | Fine-grained PAT named `rbi-archive-actions`, this repo only, Contents: Read and write, 90-day expiry. Used by checkout and push steps. Cannot push `.github/workflows/` and cannot dispatch workflows. | Set 13 Nov 2026 |
| `GPG_PRIVATE_KEY` | The user's personal GPG private key, for signing every pipeline commit. | Set 13 Nov 2026 |
| `GPG_PASSPHRASE` | Passphrase for the GPG key. | Set 13 Nov 2026 |
| `HF_TOKEN` | Hugging Face fine-grained write token (named "MUSE"). Used by the weekly sync to backfill new PDFs to Hugging Face. | Added by the user 13 Nov 2026 ~12:25 IST |

- Optional later nicety, NOT a blocker: upgrade `GH_PAT` to add Workflows and Actions read/write. Report it as an option in the final report; do not block on it.
- The Hugging Face token itself is held in the Secure Vault and reached only through the surrogate at `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`. Never log the token or any presigned S3 URL. Never ask the user for the token in chat.

---

## 6. Commit identity and GPG signing (proven setup — do not redesign)

- **Signing is OpenPGP (GPG), NOT SSH.** The machine was explicitly switched from SSH signing to OpenPGP during setup. Do NOT reintroduce SSH signing, and do NOT use the secret names from the original pasted directive (`USER_GH_PAT`, `GIT_SIGNING_SSH_PRIVATE_KEY`, `GIT_SIGNING_SSH_PUBLIC_KEY`). The real secret names are in Section 5.
- **GPG key:** id `E3A0ABB6FBEC5840`, RSA 4096, fingerprint `6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840`, UID Souvik Dey `<imsovikde@gmail.com>`, created 2026-11-13, expires 2028-11-12. Signing subkey `72BA468A855F34E2`.
- **Workflow mechanism (proven):** `crazy-max/ghaction-import-gpg@v6` imports the key from `GPG_PRIVATE_KEY` + `GPG_PASSPHRASE`, and `actions/checkout@v4` checks out with `GH_PAT`. The setup report explicitly says: replace the placeholder step with the real ingestion step; keep the signing and commit steps as they are.
- **Proof:** the four setup commits (`96291352`, `abced89b`, `e868454d`, `e0533340`) are all authored AND committed by Souvik Dey `<imsovikde@gmail.com>`, login imsovikde, id 153044727, and the repo's own `GPG-SETUP-REPORT.md` records API proof: run `43377069291` green, commit `e053334` → `verified: true, reason: valid`. The pipeline bundle commit `a690935` is likewise Verified.
- **How to verify a commit:** raw GitHub API JSON DOES show `commit.verification.verified`. Fetch `https://api.github.com/repos/imsovikde/rbi-regulatory-archive-1991-2026/commits/<sha>` and check `commit.verification.verified == true`, `commit.verification.reason == "valid"`, and `author.login == "imsovikde"`. (The Muse GitHub connector's `get_commit` shows no verification field, and the commit page text fetch omits the badge — use the raw API.)
- **Author name/email alone is NOT Verified.** `GITHUB_TOKEN` commits are `github-actions[bot]`. Verified from Actions requires the user's private signing key in a repo secret, as set up here.
- **The pre-existing workflow `archive-update.yml`** (daily cron `0 3 * * *` + workflow_dispatch, same proven GPG steps) still runs daily alongside the new pipeline. Both push with rebase, so they coexist. Mention this in the final report.

---

## 7. Architecture (decisions already made — do not relitigate)

### 7.1 Folder names and parity

- **1:1 path/filename parity is the rule.** Each Hugging Face PDF maps to an identically named `.md` file in the same relative folder/year hierarchy in the GitHub repo under `data/`. Example: Hugging Face `Press-Releases/2025/2025-01-01_Press-Releases_59431_….pdf` becomes `data/Press-Releases/2025/2025-01-01_Press-Releases_59431_….md`.
- **Hugging Face folder names are preserved exactly:** `Master-Directions`, `Notifications`, `Master-Circulars`, `Draft-Notifications-Guidelines`, `Circulars`, `Press-Releases`. The original directive's §5 showed renamed folders (`01_Master_Directions/` etc.). That conflicts with §1.1 parity; parity wins. Numbered labels live only inside index files, never as folder names. Record this as a documented deviation.
- **Per-category counts (total 88,236):** Master-Directions 397, Draft-Notifications-Guidelines 546, Master-Circulars 1,013, Notifications 10,527, Circulars 11,690, Press-Releases 64,063.
- **Earliest year with files is 1992.** 1991 stubs exist but are empty by design (no PDFs). Do not "fix" 1991.
- **Manifest CSV uses short category labels; Hugging Face folders use long names.** The mapping is verified 1:1 (category field in the ledger is the folder name).

### 7.2 Indexes (the centerpiece — all must be 100% populated at completion)

- Root: `llms.txt`, `llms-full.txt`, `INDEX.md`, `README.md` (live progress dashboard), `PROGRESS.md`, `STATE.json`.
- Category-level and per-year `INDEX.md` files.
- `manifest/catalog/<YYYY>.jsonl` (one shard per year; the old single `manifest/master_catalog.jsonl` was deleted in Defect 7, commit `60977d2`) and `manifest/sha256_conversion_ledger.csv`.
- Sharded JSON: `index/by_year/<YYYY>.json`, `index/by_category/<category>.json`, `index/url_to_path_map.json`, `index/url_collisions.json`.
- **URL map fact:** only 81,828 PDF URLs are unique. The map holds 170,064 keys, not 176,472. **5,951 RBI URLs map to more than one Markdown file.** The map holds the first path in sorted order per URL; every path is preserved in `index/url_collisions.json`. Do not "deduplicate" this away.
- Seed files already in the repo (landed by bootstrap): `manifest/hf_88236_inventory.jsonl` (88,236 rows), `manifest/catalog/<YYYY>.jsonl` (sharded by year since Defect 7; the old single `manifest/master_catalog.jsonl` was deleted, commit `60977d2`), `manifest/sha256_conversion_ledger.csv` (88,236 PENDING rows, 20 columns — see Section 9), `manifest/pdf_final_direct_urls.txt` (byte-identical copy, 81,828 URLs), `index/by_year/`, `index/by_category/`, `index/url_to_path_map.json`, `index/url_collisions.json`, `llms.txt`, `llms-full.txt`, `INDEX.md`, `PROGRESS.md`, `STATE.json` (total 88,236, done 0), `.gitignore` (includes `__pycache__/`, `.cache/`, key-material blocks, plus `!data/` `!manifest/` `!index/` guards).

### 7.3 Repository layout

```
README.md  PROGRESS.md  STATE.json  llms.txt  llms-full.txt  INDEX.md
manifest/  (hf_88236_inventory.jsonl, catalog/<YYYY>.jsonl, sha256_conversion_ledger.csv, pdf_final_direct_urls.txt)
index/     (by_year/, by_category/, url_to_path_map.json, url_collisions.json)
data/      (Master-Directions/, Notifications/, Master-Circulars/, Draft-Notifications-Guidelines/, Circulars/, Press-Releases/ — .md files, 1:1 with HF)
src/rbi_pipeline/  (hf_enumerator.py, rbi_crawler.py, converter.py, verifier.py, indexer.py, git_committer.py, runner.py, __init__.py)
scripts/   (register_new_documents.py, audit_parity.py, setup_verified_signing.sh)
docs/      (converter-test-report.md, CONTEXT-TRANSFER.md — this file)
.github/workflows/  (00_bootstrap.yml, 01_continuous_conversion.yml, 02_weekly_rbi_hf_github_sync.yml, 03_integrity_audit.yml, archive-update.yml)
sync/      (registered.json — created by weekly sync runs)
```

---

## 8. Conversion stack and algorithm (mandatory)

### 8.1 Stack

- **Tier 1 (native): firecrawl/anydoc + PyMuPDF.** anydoc is VERIFIED working: `pip install firecrawl-anydoc` installs 0.2.4 cleanly; `to_markdown_bytes(data, ocr="reject")` converts real RBI PDFs with clean GFM tables. PyMuPDF is the fallback.
- **Tier 2 (OCR): RapidOCR (PP-OCRv5 ONNX), via `rapidocr-onnxruntime` 1.4.4.** This is the proven engine. **PaddleOCR proper was NOT installed or tested** — do not claim it was. PaddlePaddle, PaddleX, and onnxruntime belong to this tier as specified.
- **Tier 3:** OCRmyPDF, Tesseract (eng+hin).
- **Tier 4:** Pillow, Ghostscript, Poppler.
- **Tier 5:** SymPy, DejaVu fonts.
- **Docling and MinerU are STRICTLY EXCLUDED as truth sources.** Never use them for conversion output.
- **Test evidence (converter test, 13 November 2026):** 14 real PDFs, 180 pages, all 14 verification OK, all PDF SHA-256 matched the manifest, all md_sha256 independently recomputed and matched, all `VERIFIED_LEVEL_5`. Total 24.9 s (native ~0.02 s/page; OCR ~5–7 s/page). Mean Markdown size 22,826.7 bytes/PDF → projected total ≈ 2.01 GB decimal (1.88 GiB). Native-only mean 17,690 bytes → ~1.56 GB. Mean time 1.78 s/PDF single-thread → ~43.5 h projection for 88,236 files; native-only 0.16 s/PDF. Full detail: `docs/converter-test-report.md` in the repo (and `pipeline-build/TEST-REPORT.md` locally).
- **Honest gaps from that test:** the four "old scanned" test files were actually born-digital (0 OCR pages). Notifications/1991 and /1995 have zero PDFs on disk (BLOCKED), so they are untestable. The OCR path is proven on two mixed files (2002: 53 pages / 3 OCR; 2005: 8 pages / 1 OCR). RapidOCR merges words without spaces on decorative title pages. Three OCR pages produced no text from either engine; hand-verified genuinely blank or a signature/logo graphic, so `<!-- OCR_EMPTY_PAGE -->` is correct there. Ghostscript repair path is written but never triggered. Tesseract on the local VM is eng-only (no hin); the Actions workflow installs `tesseract-ocr-hin`. anydoc renders bilingual press-release mastheads with some Hindi mojibake; the English body and figures are clean.

### 8.2 Converter algorithm (`src/rbi_pipeline/converter.py`, 5 stages)

1. SHA-256 + PyMuPDF page count + Ghostscript repair.
2. anydoc native extraction + per-page character-density audit (under 30 alphanumeric characters + raster images = NEEDS_OCR).
3. Hybrid OCR: OCRmyPDF + RapidOCR/Tesseract; 300 DPI rasterisation → PaddleOCR-family engine; merge in exact page order with `<!-- PAGE N -->` anchors.
4. Level-5 verification: 100% page coverage, SymPy formula parse, GFM table pipe balance, non-empty density.
5. YAML frontmatter + atomic write.

Frontmatter fields (all required): `doc_id`, `title`, `category`, `year`, `source_hf_url`, `source_rbi_url`, `pdf_sha256`, `md_sha256`, `total_pages`, `native_pages`, `ocr_pages`, `conversion_engine`, `converted_at_utc`, `verification_status` (`VERIFIED_LEVEL_5`).

### 8.3 Batch and commit format

- **Micro-batches of 50–100 PDFs per commit. Default batch size 75.**
- Batch commit message format (exact):
  `chore(convert): [XX.XXXX%] <done>/<total> PDFs -> MD | <Category>/<Year> Batch #<N> | <native_count> anydoc + <ocr_count> OCR verified`
- Index rebuild commit message: `chore(index): rebuild indexes | <done>/<total> PDFs -> MD`
- Sync commit message: `chore(sync): <n> new RBI documents -> MD | <date> | imsovikde verified`
- Never force-push. `commit -S`, `pull --rebase origin main`, `push origin HEAD:main`, maximum 3 retries, minimum 5 s pacing between attempts.

---

## 9. Runner and orchestration (`src/rbi_pipeline/`)

- **Runner CLI defaults:** `--manifest manifest/hf_88236_inventory.jsonl`, `--batch-size 75`, `--max-runtime-seconds 17400`, `--state STATE.json`, `--ledger manifest/sha256_conversion_ledger.csv`, `--repo-root .`, `--workers 2`.
- **Time budget = max-runtime minus 600 s reserve.** A 600 s budget run exits immediately by design.
- **Per-file failures become FAILED ledger rows; they never kill the batch.** NEEDS_REVIEW files still count as DONE.
- **Stop after 3 consecutive zero-conversion batches** (RuntimeError, exit 2). The workflow's self-chain step is gated on the convert step succeeding, so a failed run does not chain. The 6-hour watchdog cron retries failed runs.
- **Index rebuild (`indexer.build_all`) runs once at graceful stop** and is committed as its own signed commit (Section 8.3), staging INDEX.md, README.md, llms.txt, llms-full.txt, manifest/catalog/*.jsonl, index/url_to_path_map.json, index/url_collisions.json, index/by_year/*, index/by_category/*, plus STATE.json. A startup recovery commit handles an uncommitted rebuild from a previous run. A failed index commit exits 2.
- **Ledger append is an upsert.** The runner replaces the file's PENDING row in place and rewrites the file atomically (`upsert_ledger_rows`). Appending would duplicate rows and break the audit's row-count check.
- **Ledger columns (20, exact order):** file_path, md_path, category, year, listing_date, headline, document_id, pdf_url, hf_url, pdf_sha256, md_sha256, status, verification_status, engine, total_pages, native_pages, ocr_pages, source, converted_at_utc, error.
- **Guards:** 1 GiB free-disk guard; local `.cache` cleanup; runner disk at or under 10 GB; sequential conversion (the converter does not set PROCESS_SAFE).
- **`hf_enumerator`:** iterates the inventory sorted by category, then year, then listing date, then file name. `download_pdf` retries with backoff and jitter on 429/5xx, verifies `%PDF` magic, size, and SHA-256. Typed `DownloadError` on failure. HTTP client passes the proxy explicitly from the environment, `trust_env=False`, and verifies TLS with `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE` or the default bundle. Verification is NEVER disabled. On plain Actions runners (no proxy variables) it connects directly.
- **`git_committer.configure_identity`** raises unless `commit.gpgsign` is true and a signing key is configured. `commit_batch` stages exactly the given paths and raises `CommitError` for any path under `.github/workflows/`. `verify_last_commit` requires the signature status `%G?` to be G or U.
- **Push retry re-syncs (Defect 6 fix, commit `02bd3b5`):** before each retry after the first, `commit_batch` re-runs `git pull --rebase origin main`, so a push rejected because main moved is retried against the new main. A rebase conflict during a retry aborts the rebase and raises CommitError. Never force-pushes.
- **`rbi_crawler`:** `discover_new(pdf_urls_file, ledger_path)` crawls the 7 live endpoints (Section 12). Real CLI: `python3 -m src.rbi_pipeline.rbi_crawler --urls <file> --ledger <file> --out <file>` (NO subcommands). `sync_new_to_hf(new_pdfs, repo_id, token)` uploads only when `HF_TOKEN` is set.
- **`scripts/register_new_documents.py`:** downloads each new PDF once, derives the canonical name, appends the inventory row + ledger PENDING row (20-column) + direct-URL list entry, backfills to Hugging Face via `sync_new_to_hf` when `HF_TOKEN` is set (warns and continues otherwise), writes `sync/registered.json`. Idempotent (dedup against inventory + ledger + URLs file; a re-run registers 0). Headline heuristic: page-1 text, skipping masthead lines and full-line dates, skipping parenthetical caption lines; first substantial line of 4 or more words. Tested end to end on the 59431 press release: correct category Press-Releases, date 2025-01-01, headline "Money Market Operations as on December 31, 2024".
- **Known limits of the register script (recorded, not bugs):** the headline comes from the PDF's page 1 (the crawler does not record the listing page), and a new press release's document_id is the PDF file stem (a hash) rather than the numeric listing ID. The file is still uniquely named, converted, and indexed; both values are recorded in `sync/registered.json` with their source.
- **`scripts/audit_parity.py` (workflow 03):** 4 checks — A: ledger DONE rows have a valid `.md` file; B: STATE counts match the ledger; C: last commit authored by Souvik Dey; D: `url_to_path_map` covers every `pdf_url`. Commits `AUDIT.md` only if changed; never modifies `.md` files.
- **Smoke test (local rig, 13 November 2026, PASSED):** 3 test files (first Press-Releases 2025 rows), STATE total 3, 5 commits, all signed with a THROWAWAY test GPG key (fingerprint `CF1653A721B797EDFF9C17176A0BFEB2360F4424`, "Smoke Test <smoke-test@example.invalid>", no passphrase). That key is test identity ONLY. Never push smoke commits anywhere; the smoke repo is local-only. The smoke test found and fixed 5 integration bugs (index-rebuild stall, httpx missing in the venv, httpx proxy/SSL bug, ledger append-vs-upsert, all-failed-batch infinite loop). Full detail is in Section 14. The inventory JSONL `year` field is an integer (2025), not a string.
- **Environment note:** `/tmp` on the local VM is a 512 MB tmpfs with only ~268 MB free. Local test runs must use the workspace, not `/tmp`.

---

## 10. Workflows

### 00 — Bootstrap Pipeline (imsovikde Verified) — `00_bootstrap.yml`

- Trigger: `workflow_dispatch` only. Concurrency group `rbi-markdown-conversion-pipeline` (shared with 01 and 02 — Defect 5 fix), cancel-in-progress false. Timeout 120 minutes.
- Steps: checkout with `GH_PAT` → import GPG signing → download the bundle from Hugging Face `_pipeline/bootstrap/` using MANIFEST.txt → copy everything EXCEPT `.github/workflows/` → commit as Souvik Dey (Verified) → push → dispatch workflow 01 as the pilot (batch_size 75, max_batches_per_run 2, self_chain false).
- Preserves live progress files: if STATE.json `done_count` is greater than 0, existing progress is kept, not overwritten.
- Already ran once (run 43383089432, failed only at the dispatch step — Defect 1). Re-run it after the fix, or dispatch the pilot directly; either is correct.

### 01 — Continuous RBI PDF-to-Markdown Conversion (imsovikde Verified) — `01_continuous_conversion.yml`

- Triggers: `workflow_dispatch` (inputs batch_size default "75", max_batches_per_run default "200", self_chain default "true") AND schedule watchdog cron `15 */6 * * *`.
- Timeout 330 minutes. `MAX_RUNTIME_SECONDS` 17400 (290 minutes; flush and chain at 290 minutes).
- Apt deps include tesseract-ocr-hin, ghostscript, poppler-utils, fonts-dejavu, qpdf. Python 3.11. Pip install in two groups, with `|| true` on the heavy OCR group.
- Concurrency group `rbi-markdown-conversion-pipeline`, cancel-in-progress false. Shared with 00 and 02 (Defect 5 fix): all workflows that push to main serialize behind this one group, so two of them can never push at once. Do not give 00, 01 or 02 a separate group.
- Flow: setup → install stack → run the runner (per-batch signed commits) → at the time limit, flush, rebuild indexes, commit STATE.json → if remaining work is greater than 0, fire `gh workflow run 01_continuous_conversion.yml --ref main` (self-chain, via `GITHUB_TOKEN`). Self-chain requires Defect 1's fix.
- Checkout pins `ref: main` (Defect 4 fix, commit `b2a9380`, 13 Nov 2026): a run dispatched while another is active checks out the tip of main when its job starts, never the stale dispatch-time commit. Do not remove this line.
- Pilot settings: batch_size 75, max_batches_per_run 2, self_chain false = 150 files, no auto-chain. The pilot exists so a human verifies the first Markdown files and Verified commits before the full run is dispatched by hand. Do not raise these numbers in a pilot dispatch.

### 02 — Weekly RBI Hugging Face to GitHub Sync — `02_weekly_rbi_hf_github_sync.yml`

- Triggers: schedule Monday 02:00 UTC (Hugging Face side sync) and 02:30 UTC (GitHub workflow); also `workflow_dispatch`.
- Concurrency group `rbi-markdown-conversion-pipeline` (shared with 00 and 01 — Defect 5 fix), cancel-in-progress false. A weekly sync run waits behind an active conversion run, so the two can never push to main at once.
- Flow, using only real, tested CLIs:
  1. Discover: `python3 -m src.rbi_pipeline.rbi_crawler --urls manifest/pdf_final_direct_urls.txt --ledger manifest/sha256_conversion_ledger.csv --out .cache/sync/new_documents.json`. **Mandatory direct RBI fallback crawl even if Hugging Face shows zero new.**
  2. Register: `scripts/register_new_documents.py` (Section 9). Backfills to Hugging Face when `HF_TOKEN` is set.
  3. Convert: a normal runner pass (new rows are pending in the inventory; STATE total grows from 88,236 by the new count).
  4. Final commit: stages only `manifest/hf_88236_inventory.jsonl`, `manifest/pdf_final_direct_urls.txt`, `sync/registered.json` (the runner already committed the `.md` files, ledger, STATE, and indexes). A zero-new week commits nothing.
- This is the automatic Hugging Face path: new RBI PDFs are fetched by this workflow and backfilled to Hugging Face automatically. No manual upload step exists or is needed.

### 03 — RBI Archive Integrity Audit — `03_integrity_audit.yml`

- Trigger: schedule Sunday 03:00 UTC + `workflow_dispatch`.
- Runs `scripts/audit_parity.py` (Section 9), commits `AUDIT.md` only if changed, never modifies `.md` files.

### Pre-existing — `archive-update.yml`

- Daily cron `0 3 * * *` + workflow_dispatch. Proven GPG steps. Runs daily alongside the new pipeline; both push with rebase, so they coexist.

---

## 11. Hugging Face (PDF store — complete; keep it current automatically)

- Dataset: `imsovikde/rbi-regulatory-archive-1991-2026`, public. Page: https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026
- Direct file download (no login): `https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/<Category>/<Year>/<file>.pdf`
- Tree API and dataset info endpoint exist; the connector doc records the exact calls.
- **Upload mechanics (do not improvise):** the single-file upload endpoint is retired (HTTP 410). The only route is preupload → LFS batch → presigned PUT → commit endpoint. Helpers live in the connector directory (`~/workspace/custom-connectors/custom.huggingface/bin/`: `hf.py`, `upload.py`, `verify_upload.py`, `stage6_verify.py`, `fix_gitattributes.py`, `commit_file.py`, `post_discussion_comment.py`). Connector doc: `~/workspace/custom-connectors/custom.huggingface/CONNECTOR.md` — reread it before using the connector again.
- **Known quirks:** dataset creation is `POST /api/repos/create` with `{"type":"dataset","name":<name-only>,"private":false}`. `hf.py` output truncates at 8,000 characters. The Hugging Face token is reached only through the Secure Vault surrogate; never log the token or presigned S3 URLs.
- **`.gitattributes`:** it grew to 10,440,282 bytes during upload and Hugging Face rejects pushes over 10 MiB. Fixed with 60 header lines + one `*.pdf filter=lfs` wildcard (commit `df6e03c9`). Do not let it regrow with per-file lines.
- **Data card (README.md, commit `6a5364b7`, 9,777 bytes):** YAML verified live — license `other`, pretty_name "RBI Regulatory Archive 1991-2026", language en, 12 tags, size `10K<n<100K`, config `manifest` → `data/manifest.csv`. Local source: `~/workspace/rbi-archive-muse/_manifests/hf-dataset-README.md`.
- **Viewer manifest (`data/manifest.csv`, commit `f2342995`):** 92,100 rows, 52,226,593 bytes, SHA-256 `42ed9f65bf561e4046f49ccc1d0abd139c755e3503cb551c6ccfb6ce0f8b6fa2` (remote LFS oid matches exactly). Clean public schema; the `drive_file_id` column was stripped. Local copy: `~/workspace/rbi-archive-muse/data/manifest.csv`.
- **Discussion endpoints (recorded in CONNECTOR.md):** POST comment = `/api/datasets/{repo}/discussions/{num}/comment` → 201. Hide = POST `…/discussions/{num}/comment/{comment_id}/hide` → 200. GET discussion returns `events`; comment text is at `event.data.latest.raw`.
- **Full upload history:** pilot Master-Directions 396/396 verified. Full run stages 1–5 uploaded Draft-Notifications-Guidelines 546, Master-Circulars 1,013, Notifications 10,525, Circulars 11,690, Press-Releases 64,050. Stage 6 final verification PASSED 19:49 UTC 12 November 2026: local 88,220 / remote 88,220, 0 missing/extra/SHA-256 mismatch, spot re-hash 120/120. 456 commits, head `827cfe78`, usedStorage 15,396,152,528 bytes. Incidents, zero files lost: one runtime restart during Stage 3; three SIGTERM kills during Stage 5 (relaunched detached via nohup). Logs: `~/workspace/rbi-archive-muse/_manifests/hf-upload/`. Nothing was deleted locally.

## 12. RBI sources and endpoints (official RBI site only)

- **PDF hosts:** `rbidocs.rbi.org.in` serves 84,775 files; `www.rbi.org.in` serves 3,461.
- **Entry points (5):**
  - `https://rbi.org.in/scripts/NotificationUser.aspx`
  - `https://rbi.org.in/scripts/DraftNotificationsGuildelines.aspx`
  - `https://rbi.org.in/scripts/BS_CircularIndexDisplay.aspx`
  - `https://www.rbi.org.in/commonman/english/Scripts/PressReleases.aspx`
  - `https://www.rbi.org.in/commonman/english/Scripts/Notification.aspx`
- **Live endpoints for the weekly sync (7):**
  - Master Directions: `https://www.rbi.org.in/Scripts/BS_ViewMasterDirections.aspx`
  - Notifications: `https://www.rbi.org.in/Scripts/NotificationUser.aspx`
  - Master Circulars: `https://www.rbi.org.in/Scripts/BS_ViewMasterCirculardetails.aspx`
  - Drafts: `https://www.rbi.org.in/Scripts/DraftNotificationsGuildelines.aspx`
  - Circular Index: `https://www.rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx`
  - Press Releases: `https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx`
  - Document host: `https://rbidocs.rbi.org.in/rdocs/`
- **Dating rule (fixed after the first retry pass misdated 3 items):** date from the page-1 header only.
- **Crawler counts vs manifest:** per-prefix URL counts in the original directive differ slightly from measured counts. The manifest file is the source of truth.
- **Reachability note:** `rbidocs.rbi.org.in` is currently unreachable from the local VM (curl HTTP 000 / empty reply). Hugging Face is the primary source and works; the RBI fallback is a bonus, not a dependency. The weekly sync still attempts the direct RBI crawl every week.

## 13. Local filesystem map and isolation

- **This run's local staging (intact, the recovery store):** `~/workspace/rbi-archive-muse/`
  - `_manifests/` — INVENTORY.csv, SHA256_MANIFEST.csv, PROGRESS.log, FINAL_REPORT.md, RETRY-REPORT-2026-11-13.md, unavailable_pdf_entries.csv, bot_blocked_urls.json, dead_links.json, gap_dating.csv, retry_state.jsonl, pdf_source_endpoints.md, pdf_final_direct_urls.txt, scripts/, hf-upload/ logs, backups/2026-11-13-merge/, hf-dataset-README.md
  - `_pipeline/bootstrap/` — the bundle copy staged for Hugging Face (74 files with MANIFEST.txt)
  - `data/manifest.csv` — local copy of the viewer manifest
  - `pipeline-build/` — src/, repo/ (bundle), MANIFEST.txt, TEST-REPORT.md, smoke/, venv/, run_tests.py, test-output/
  - `github-ready/repo/` — STALE scaffold. Do NOT push as-is.
- **THE OTHER AGENT'S RUN — NEVER TOUCH:** Drive folder `RBI_Regulatory_Archive_1991_2026__Muse`, ID `1ikGeQwJJwMXsJMu92IoXBGLwcS-ZnJYC`; local `~/workspace/rbi-archive/`. Never read, list, copy, link to, or reuse anything from it. The two runs are reported separately and never merged.
- **This run's old Drive root** was `RBI-Regulatory-Archive_Muse`, ID `1O_PyWdkyMhob4QtdAfgQSDAfSUxyxyyda`. Deleted by the user on 11 November 2026. Do not recreate it or restore files to Drive unless the user explicitly orders it.
- **Drive listing caution (learned the hard way):** Drive `files.list` silently truncates and undercounts. A pageSize-100 listing caps at exactly 100; pageSize 200 caps at 200; a full paginated listing once returned only 308 of a folder's 628 verified files, and summed 12.71 GB against 23.67 GB of real usage. Never present a listing-derived total as the Drive total; always cross-check against `about.get` usageInDrive and state the gap.
- **`/tmp` is a 512 MB tmpfs.** It was wiped mid-task once, deleting a complete 37,720-file Drive listing. Save all intermediates under `~/workspace/`, never `/tmp`.

## 14. Known bugs, fixes applied, and open limitations

### Fixed (do not reintroduce)

1. **HF upload, duplicate commits:** 490 regular (non-LFS) Notifications files were committed twice with identical bytes. Fixed by matching the skip check on oid OR size. Stage 3 commit titles overstate the overall count by up to 490; the verified count is the truth.
2. **HF upload, .gitattributes too large:** grew past 10 MiB and Hugging Face rejected pushes. Fixed with a wildcard (Section 11).
3. **Smoke-test fix 1:** an uncommitted index rebuild stalled the pipeline (the next `git pull --rebase` failed on unstaged changes). The runner now commits the rebuild as its own signed commit, plus a startup recovery commit for a rebuild left over from a previous run.
4. **Smoke-test fix 2:** `httpx` was missing in the test venv (the enumerator fell back to RBI URLs). Installed; the production workflow pip-installs it.
5. **Smoke-test fix 3:** httpx proxy bug — the VM's NO_PROXY contains bracketed IPv6 entries (`[::1]`), which broke httpx URL parsing; with `trust_env=False` it then dropped the TLS bundle and failed verification. Fixed in `hf_enumerator._http_client` (proxy passed explicitly from the environment, `trust_env=False`, TLS verified from `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE` or the default; verification is NEVER disabled). `rbi_crawler` uses the same helper.
6. **Smoke-test fix 4:** the runner appended a DONE row per conversion, duplicating the seed PENDING row (the ledger would have reached 176,472 rows). Fixed with the upsert (Section 9). The production seed ledger was regenerated to the runner's exact 20-column format with 88,236 PENDING rows.
7. **Smoke-test fix 5:** an all-failed batch committed empty and retried the same pending files until the time budget expired. Fixed: stop after 3 consecutive zero-conversion batches; the workflow self-chain step is gated on the convert step succeeding.
8. **Workflow 02 CLI mismatch:** the original 02 invoked CLI forms that do not exist (`rbi_crawler discover` / `backfill-hf` subcommands, `runner --sync-only --new-documents`, `indexer --rebuild`). It was rewritten to real, tested CLIs plus `scripts/register_new_documents.py` (Section 9).
9. **`rbi_crawler.derive_canonical_name`** gained a `category` parameter (the register script passes the crawler's classification instead of re-guessing from the bare PDF URL).
10. **Defect 4 (stale checkout rebase conflict):** see Section 4. Fix: `ref: main` in the checkout step of 00/01/02 (commit `b2a9380`, 13 Nov 2026). Do not remove `ref: main`.
11. **Defect 5 (separate concurrency groups):** see Section 4. Fix: 00/01/02 share the group `rbi-markdown-conversion-pipeline`. Do not give 00, 01 or 02 a separate group.
12. **Defect 6 (push retry never re-syncs):** see Section 4. Fix: `commit_batch` re-runs `git pull --rebase` before each push retry (commit `02bd3b5`). Operating rule: do not push to main while a conversion run is active unless the push is required to fix the run itself.
13. **Defect 7 (catalog over 100 MB):** see Section 4. Fix: catalog sharded by year into `manifest/catalog/<YYYY>.jsonl` (commits `60977d2`, `7389e3a`, `cc6f16f`). Never re-create a single `manifest/master_catalog.jsonl`. Watch the ledger (~72 MB at completion) and `index/url_to_path_map.json` (~25 MB) as the next size risks.
14. **GitHub API access (added 14 Nov 2026):** the user gave a fine-grained PAT via the Secure Vault; it lives as connection `custom.github` (never in a file, never in chat). Helper: `~/workspace/custom-connectors/custom.github/bin/gh.py` (`whoami`, `run <id>`, `runs [n]`, `dispatch`, `commit <sha>`, `file <path>`); doc: `~/workspace/custom-connectors/custom.github/CONNECTOR.md`. It is for READS and dispatching only — API commits are unsigned, so it must never push to main (Verified commits come only from the Actions runner's GPG signing and the web UI). The shared-IP unauthenticated rate limit (60 req/hr) no longer applies to these calls.

### Open limitations (recorded, not defects)

- PaddleOCR proper was NOT installed or tested; RapidOCR (PP-OCRv5 ONNX) is the proven OCR engine.
- RapidOCR merges words without spaces on decorative title pages.
- Three OCR pages in testing produced no text from either engine; hand-verified genuinely blank or a signature/logo graphic.
- Ghostscript repair path is written but never triggered in testing.
- Tesseract on the local VM is eng-only; the Actions workflow installs `tesseract-ocr-hin`.
- anydoc renders bilingual press-release mastheads with some Hindi mojibake; English body and figures are clean.
- Notifications/1991 and /1995 have zero PDFs on disk (BLOCKED); untestable.
- The register script's headline comes from the PDF's page 1, and a new press release's document_id is the PDF file stem (a hash), not the numeric listing ID (Section 9).
- The four "old scanned" converter-test files were actually born-digital; the OCR path is proven only on two mixed files.
- The Hugging Face Parquet viewer table was not confirmed live at last check (Section 3.1).
- The Verified badge is not visible through the Muse GitHub connector's `get_commit` (no verification field); use the raw API JSON (Section 6).
- `archive-update.yml`'s daily cron coexists with the pipeline; both push with rebase.

## 15. Verification gates and completion criteria

- **G0–G8 + Ralph Loop (from the original directive).** COMPLETE only when all gates pass in one pass. The original download run passed G0, G2–G6; G1 failed only on post-freeze items (now merged); G7 failed only because the Drive copy was deleted (Drive is out of scope now).
- **Final gate (all must hold):**
  - `total_markdown_files == 88,236`.
  - Every `.md` has valid frontmatter, SHA fields, and page parity with its PDF.
  - All indexes 100% populated (Section 7.2).
  - All 3 workflows (01, 02, 03) active and passing.
  - Every commit on `main` Verified under imsovikde.
- **Audit script:** `scripts/audit_parity.py` checks A (ledger DONE rows have a valid `.md`), B (STATE counts match the ledger), C (last commit authored by Souvik Dey), D (`url_to_path_map` covers every `pdf_url`).
- **Reporting rules:** report archive progress only as verified counts with the delta stated. Never claim completion until the gates prove it. Every substantive response ends with a short TLDR. When the user asks for a concise and comprehensive version, brevity is part of the instruction, not a trade-off against completeness: verification depth stays, presentation is compressed.
- **Throughput and ETA (measured, state as estimates):** converter test mean 1.78 s/PDF single-thread → ~43.5 h projection; native-only 0.16 s/PDF. Projected Markdown total ≈ 2.01 GB decimal (1.88 GiB). Re-measure from the pilot's real throughput and restate the ETA; do not repeat these numbers as fact after the pilot.

## 16. Runbook for the receiving agent (do these in order)

1. **Clone** `https://github.com/imsovikde/rbi-regulatory-archive-1991-2026` (branch `main`). Read the live state: recent commits, workflow runs, `STATE.json`, `README.md`, `PROGRESS.md`. Reconcile with Section 3; where live state disagrees, live state wins and you update Section 3.
2. **Commit this file** to the repo at `docs/CONTEXT-TRANSFER.md` (message `docs: add living context transfer file`, authored by Souvik Dey, GPG-signed). Verify it landed and is Verified.
3. **Apply Defect 1 and Defect 2 fixes** (Section 4). Edit `00_bootstrap.yml`, `01_continuous_conversion.yml`, `02_weekly_rbi_hf_github_sync.yml` in your local copy. Re-validate all four workflow files as YAML after every edit.
4. **Re-land the three edited workflow files via the GitHub web UI** (exact names, byte-for-byte, one commit to `main`). Verify each landed file by SHA-256 against your local copy. Record the post-fix SHA-256 values in Section 3.
5. **Re-run the bootstrap** (workflow 00, workflow_dispatch) OR dispatch the pilot directly (workflow 01: batch_size 75, max_batches_per_run 2, self_chain false). Verify the run's conclusion and read the failing step's log in the browser if it fails again — report the exact error text before trying anything else.
6. **Verify the pilot:** 150 Markdown files exist under `data/` with valid frontmatter and page parity; the batch commits follow the Section 8.3 message format; every pilot commit is Verified under imsovikde (raw API check, Section 6); `STATE.json` reads done 150 / total 88,236; `README.md`, `PROGRESS.md`, and the indexes show the live percentage. Spot-check at least 3 Markdown files against their PDFs (one native, one mixed/OCR, one old).
7. **Dispatch the full run** (workflow 01, defaults: batch_size 75, max_batches_per_run 200, self_chain true). Confirm the self-chaining loop is running: when run N finishes with remaining work, run N+1 is dispatched automatically.
8. **Monitor to 100%.** After each run, verify the new STATE counts and the latest commits. If a run fails, diagnose from the failing step (never from a guess), fix, and re-dispatch. If any commit is unsigned or bot-authored, stop, report it, and do not proceed until the signing path is fixed.
9. **Run the final gate** (Section 15). Verify `total_markdown_files == 88,236`, frontmatter and page parity across the set, indexes 100% populated, workflows 01/02/03 passing.
10. **Update this file** (Section 17) with the final verified state, the measured throughput and ETA, the deviations (GPG not SSH; Hugging Face folder names preserved; web-UI commits are GitHub-web-flow Verified vs pipeline commits signed with the personal GPG key), the URL-collision finding, the HF_TOKEN note, the PAT-scope note, and the register-script naming limits. Commit the updated file. Then deliver the final report to the user with a TLDR.
11. **Lower priority, only on the user's go-ahead:** re-check the Hugging Face Parquet viewer table; build the Cloudflare query layer; create the Internet Archive durability mirror; build a Hugging Face Space search UI.

## 17. Living-document protocol (future-proofing — this file must stay current)

This file is the single source of truth for the repository's context. It stays useful only if every agent that works on the repo updates it. Rules:

1. **Update at the end of every session** in which a fact in this file changes: new run, new failure, new count, new decision, new secret, new deviation. Update the "Last updated" line at the top and the dated state block in Section 3.
2. **Append, do not silently overwrite.** When a value changes, keep the old value struck through with its date (e.g. `~~88,220 PDFs~~ → 88,236 PDFs, 13 Nov 2026`). History is evidence.
3. **Record every new defect the same way Section 4 records the current two:** fact, evidence, exact fix, how it was verified.
4. **Record every new decision** with its date, who made it, and what it supersedes.
5. **The weekly sync keeps Hugging Face current automatically** (Section 10, workflow 02). After any weekly sync that registers new documents, update Section 3 counts (STATE total, per-category counts, manifest rows) and commit the updated file.
6. **If a future agent finds this file disagreeing with live GitHub state,** live state wins for counts, and the agent must reconcile the file in the same session.
7. **Never record a secret value in this file.** Names only, always.
8. **Never record a proposed action as completed.** A fix is recorded only after its verification step passes.

## 18. User preferences and standing rules

- Call him Rohit. Souvik Dey appears only on legal filings and case records, never in conversation.
- English-only responses by default; other languages only on explicit request.
- Direct, blunt, unvarnished feedback. No marketing framing, sugarcoating, filler, or vague commentary. Independent assessments with flagged contradictions. Never reverse an evaluation because a question was reframed.
- Verify-then-assert as law: read the full correspondence, page past truncated search caps, never derive dates or identifiers from dictation or memory, distinguish similar-but-different events, cite email times in IST.
- Case and legal deliverables are beautified, readable PDFs; another format only when he names it.
- Do not send, file, or pay anything without his explicit instruction.
- Completely free options only. He has repeatedly rejected anything paid.
- When a draft fails him, he takes the pen himself: hand over the verified points with file sizes, metadata, and SHA-256 values so he can write it himself. Do not rewrite after being told to stop.
- Surgical rewrites: change only what is wrong, disclose exactly what changed, prove fidelity with verifiable diffs, character counts, or byte-identical lines. Assertions of fidelity mean nothing.
- Em dashes are banned in legal drafts: use commas, hyphens, or periods. Machine-check with grep for — and – and confirm zero before delivering any legal email.
- Never deliver long email bodies in fenced code blocks in chat (they do not word-wrap on mobile). Use a plain `.txt` file attachment instead. Exception: for short email drafts he explicitly asks for a code box, because his app's code block has one-tap copy — honour the explicit request when he asks.
- Gmail: use strictly per tool rules — `+triage ... --format json` for search, `+read ... --format json` for a message, `users threads get` for a thread, one Gmail command per call, no hand-rolled parsing.
- Drafting protocol for important emails and legal text: read the ENTIRE correspondence first; extract and verify EVERY factual claim against the primary source; never trust a truncated search listing; never derive dates or identifiers from dictation, memory, or a call transcript; distinguish similar-but-different events explicitly; re-read the finished draft against the sources once more before handing it over.

---

## Appendix — exact identifiers (copy these, never retype from memory)

- GitHub repo: `imsovikde/rbi-regulatory-archive-1991-2026`, id `1456135028`, https://github.com/imsovikde/rbi-regulatory-archive-1991-2026
- Hugging Face dataset: `imsovikde/rbi-regulatory-archive-1991-2026`, id `6af59bc904804d7cc2eb5604`, https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026
- Commits: workflows `fd078a67bf531c40c944bead64aedf1fc9d273c0`; pipeline bundle `a69093552052927dce1d4e68cfea4fc556a48382`
- Runs: bootstrap `43383089432` (failed); pilot `43383873884` (failed); GPG proof run `43377069291` (green)
- HF heads: retry verification `78c006f0bd69453bd9fae3d8adb7998a6da5276c`; current `f23429951c145ad3fd35160b4be10e5f14421ded`
- HF README commit `6a5364b7`; HF manifest commit `f2342995`; HF manifest.csv SHA-256 `42ed9f65bf561e4046f49ccc1d0abd139c755e3503cb551c6ccfb6ce0f8b6fa2`
- HF upload commits: `9fd9546c`, `f8cba21e`, `9f72c862`; full-run head `827cfe78`
- Bootstrap bundle MANIFEST.txt md5: `fa23fe46d2888f34c5f01aa3555fff45`
- GPG key: `E3A0ABB6FBEC5840`, fingerprint `6AD3CFAE64F0C29C79EB4094E3A0ABB6FBEC5840`, signing subkey `72BA468A855F34E2`
- Throwaway smoke-test GPG key (NEVER use for real commits): `CF1653A721B797EDFF9C17176A0BFEB2360F4424`
- Other agent's Drive folder (NEVER touch): `1ikGeQwJJwMXsJMu92IoXBGLwcS-ZnJYC`
- Old deleted Drive root of this run: `1O_PyWdkyMhob4QtdAfgQSDAfSUxyxyyda`
- Pre-fix workflow SHA-256 values: Section 4.
- Manifest row counts: 92,100 rows total; 88,236 DOWNLOADED; 3,864 BLOCKED.
- Direct URLs file: 81,828 unique URLs.
