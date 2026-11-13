"""RBI Regulatory Archive PDF-to-Markdown conversion engine.

Engine contract:
- Input is always PDF bytes plus a metadata dict. The converter never reads
  from disk, never makes network calls, and never modifies a PDF.
- Output is GitHub-Flavored Markdown with deterministic YAML frontmatter,
  one `<!-- PAGE N -->` anchor per PDF page, in exact page order.
- Tier 1 is firecrawl-anydoc when installed; otherwise PyMuPDF text
  extraction. Tier 2 OCR runs only on pages flagged NEEDS_OCR, preferring
  RapidOCR (PP-OCRv5 ONNX) and falling back to Tesseract (eng, hin if the
  traineddata is present). Docling and MinerU are excluded as truth sources.
- Text is never invented. A page that yields nothing is emitted as its
  anchor plus `<!-- OCR_EMPTY_PAGE -->` and recorded in warnings.
- `convert_pdf` is importable without the OCR stack. All heavy imports are
  lazy, inside functions, with graceful fallback and a recorded warning.
"""

from .converter import convert_pdf
from .verifier import verify_markdown

__all__ = ["convert_pdf", "verify_markdown"]
