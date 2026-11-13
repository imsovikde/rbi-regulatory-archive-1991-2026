# PDF-to-Markdown Converter Test Report

Date: 13 November 2026. Engine: `pipeline-build/src/rbi_pipeline/` (`converter.py`,
`verifier.py`, `__init__.py`). Test runner: `pipeline-build/run_tests.py`.
Sample: 14 real PDFs from the local archive, chosen from
`_manifests/SHA256_MANIFEST.csv` (see `pipeline-build/sample.json`).
Outputs: `pipeline-build/test-output/` (14 .md files). Raw numbers:
`pipeline-build/test-results.json`.

## Environment verdict

- Python 3.12.3. System tools present: tesseract 5.3.4 (eng + osd only, no
  hin traineddata), Ghostscript 10.02.1, poppler 24.02.0, ocrmypdf 15.2.0.
- System Python is PEP 668 externally managed, so a venv was created at
  `pipeline-build/venv` (538 MB). All pip installs went there.
- PyMuPDF 2.1 installed cleanly.
- **firecrawl-anydoc: YES, installable and usable.** `pip install
  firecrawl-anydoc` installed 0.2.4 (3.5 MB wheel) with no errors, imports
  cleanly, exposes `to_markdown_bytes` and `NeedsOcrError`, and converted
  real RBI PDFs in this test. Tier 1 is anydoc, as specified, with
  `ocr="reject"` (never the hosted OCR option, no network, no key).
- RapidOCR 1.4.4 (PP-OCRv5 ONNX) installed cleanly and ran on real scanned
  pages. PaddleOCR itself was NOT installed and NOT tested; RapidOCR is the
  PP-OCRv5 path used here. SymPy 1.12 and Pillow are present.
- No Docling, no MinerU anywhere in the stack.

## Results table

| # | Class | File (short) | PDF bytes | Pages | Native | OCR | MD bytes | Time | Verifier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | born-digital MD recent | 2025-11-28 MD 13120 (Small Finance Banks, Concentration Risk) | 420,280 | 30 | 30 | 0 | 57,847 | 0.6 s | ok |
| 2 | born-digital MD recent | 2025-11-28 MD 13102 (Payments Banks, Branch Authorisation) | 615,271 | 56 | 56 | 0 | 89,380 | 0.7 s | ok |
| 3 | born-digital Notif recent | 2025-11-28 Notif 13126 (Small Finance Banks, Resource Raising) | 283,996 | 8 | 8 | 0 | 11,590 | 0.1 s | ok |
| 4 | born-digital Notif recent | 2025-12-08 Notif 13215 (Indian Currency, Nepal and Bhutan) | 145,342 | 1 | 1 | 0 | 3,286 | 0.0 s | ok |
| 5 | born-digital PR recent | 2025-12-16 PR 61824 (VRR auction result) | 225,458 | 1 | 1 | 0 | 1,999 | 0.0 s | ok |
| 6 | born-digital PR recent | 2025-12-18 PR 61847 (monetary penalty, Tamilnadu Circle Postal Co-op Bank) | 336,847 | 1 | 1 | 0 | 3,399 | 0.0 s | ok |
| 7 | Circulars | 2024-01-15 Circular DOS.ARG (Statutory Auditors, co-op banks) | 1,613,811 | 14 | 14 | 0 | 27,045 | 0.4 s | ok |
| 8 | Circulars | 2024-08-29 Circular RBI/2024-2025/71 (Interest Equalization Scheme) | 1,019,616 | 1 | 1 | 0 | 3,190 | 0.1 s | ok |
| 9 | old scanned Notif | 1992-04-21 Notif 1349 (Interest Rates on Deposits) | 33,437 | 1 | 1 | 0 | 2,749 | 0.0 s | ok |
| 10 | old scanned Notif | 1993-09-10 Notif 8798 (Delay in Crediting Instruments) | 42,630 | 1 | 1 | 0 | 2,465 | 0.0 s | ok |
| 11 | old scanned Notif | 1996-09-06 Notif 203 (Schedule IIB) | 3,372 | 1 | 1 | 0 | 1,829 | 0.0 s | ok |
| 12 | old scanned Notif | 1999-08-04 Notif 70 (A.D. Circular No.10) | 9,750 | 4 | 4 | 0 | 7,505 | 0.0 s | ok |
| 13 | mixed scanned page | 2002-10-14 Notif 909 (PMRY Master Circular) | 196,740 | 53 | 50 | 3 | 95,095 | 16.3 s | ok |
| 14 | mixed scanned page | 2005-07-01 Notif 2321 (Remittance facilities, NRIs/PIOs) | 58,038 | 8 | 7 | 1 | 12,195 | 6.6 s | ok |

Totals: 14 files, 180 pages (176 native, 4 OCR), 319,574 MD bytes, 24.9 s.
All 14 passed `verify_markdown` (page parity, table balance, density).
All 14 PDF SHA-256 values matched the manifest. All 14 carry
`verification_status: VERIFIED_LEVEL_5`. Every `md_sha256` was recomputed
independently from the written .md body and matched.

## Per-class notes (honest)

**Born-digital Master Directions (recent).** The best case. anydoc produced
clean structured Markdown with real GFM tables (rates, tenors, amounts) and
correct headings, at about 0.02 s per page. No OCR, no warnings, no repairs.
These are the bulk of the modern archive and the pipeline handles them fast.

**Born-digital Notifications (recent).** Same behaviour at smaller scale.
One-page notifications convert in under 0.1 s. Frontmatter, anchors and
hashes all verified.

**Born-digital Press Releases (recent).** One page each, trivial. One
observation: anydoc renders the bilingual RBI letterhead as a two-column
table and the Devanagari header shows mojibake in places (for example
broken glyph sequences in the Hindi masthead line). The English body, the
rates table and all figures are clean. This is a rendering fidelity note,
not a failure, and it is confined to the decorative header.

**Circulars.** The 14-page auditors circular converted fully natively in
0.4 s with balanced tables. The 1-page Interest Equalization circular was
trivial. No issues.

**Old scanned Notifications (1991-2000).** Surprise: the four files picked
as "old scanned" (1992, 1993, 1996, 1999) are actually born-digital text
PDFs, not scans. They converted natively with zero OCR pages. Two caveats
from the sample itself: Notifications/1991 and Notifications/1995 have
zero PDFs on disk at all (their census entries are BLOCKED, no PDF served
by RBI), so no 1991 or 1995 file could be tested. Old PDFs also emit
MuPDF content-stream syntax warnings on stderr (malformed 1990s streams);
PyMuPDF tolerates them and still extracts text.

**Mixed scanned pages.** This is the class that actually exercised OCR.
Both files are mostly digital with a few image pages. The 2002 PMRY
Master Circular (53 pages) had 3 OCR pages; the 2005 remittance circular
(8 pages) had 1. RapidOCR read the scanned cover page but merged words
without spaces in places (for example "PRIMEMINSTERS", "ROZGARYOJANA"),
so OCR text on decorative title pages is usable for search but not
typographically clean. Three pages produced no text from either engine:
pages 26 and 35 of the 2002 file and page 7 of the 2005 file. Those were
checked by hand: pages 26 and 35 are genuinely blank pages (0 images,
0 drawings, 0 text), and page 7 is a signature/logo graphic, so
`<!-- OCR_EMPTY_PAGE -->` is the correct honest output, not a miss.
Tesseract was tried on the blank pages and also returned nothing, which
confirms it. OCR cost dominates runtime: about 5-7 s per OCR page against
about 0.02 s per native page.

## Size projection

Mean Markdown size across the 14-file sample: **22,826.7 bytes per PDF**.
Projected total for the full archive: 22,826.7 x 88,236 = **2,014,137,962
bytes, about 2.01 GB decimal (1.88 GiB)**. Plainly stated: this is a
projection from a small stratified sample, not a measurement. The sample
over-represents long Master Directions and the two OCR-heavy files, so
the true total is likely lower; the native-only mean is 17,690 bytes per
PDF, which would project to about 1.56 GB. Either way the Markdown repo
fits comfortably inside GitHub limits if committed in micro-batches.

## Time projection

Mean conversion time: 1.78 s per PDF single-threaded, which projects to
about 43.5 hours for 88,236 files on one thread. That number is dominated
by the 4 OCR pages in the sample. Native-only files average 0.16 s per
PDF. With process-level parallelism across the runner cores and OCR
confined to flagged pages only, the real wall-clock will be far lower;
the batch design (50-100 files per commit, self-chaining runs) is still
the right shape because OCR pages are the long tail.

## Known limitations and fixes applied during testing

1. First build wrote `conversion_engine: "firecrawl-anydoc <function
   version at 0x...>"` because anydoc's `version` attribute is a function,
   not a string. Fixed: version is now read via `importlib.metadata`
   ("firecrawl-anydoc 0.2.4").
2. First build duplicated the RapidOCR entry in the engine string once per
   OCR page (a list-membership check compared the short name against full
   strings). Fixed: engine names are deduplicated by exact entry.
3. First build treated a RapidOCR empty result as final. Fixed: an empty
   RapidOCR result now falls back to Tesseract before emitting
   `<!-- OCR_EMPTY_PAGE -->`.
4. Tesseract on this VM has eng + osd only. Hindi (hin) traineddata is not
   installed, so the Tesseract fallback is English-only here. The GitHub
   Actions workflow must install `tesseract-ocr-hin` explicitly.
5. PaddleOCR proper was not installed or tested; RapidOCR (PP-OCRv5 ONNX)
   is the OCR engine proven here. PaddleOCR/PaddleX remain untested on
   this machine and must not be claimed as verified.
6. Ghostscript repair was never triggered in the sample (no file failed to
   open), so the repair path is written but untested on a real corrupt
   file. It is a fallback only and records `repair_attempted`.
7. The verifier's SymPy formula check ran (sympy 1.12 present) and
   produced no warnings on this sample; it is best-effort only by design.
