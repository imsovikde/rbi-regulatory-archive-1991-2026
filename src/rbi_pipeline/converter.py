"""Deterministic PDF-to-Markdown converter for the RBI Regulatory Archive.

Pipeline (one PDF, bytes in, Markdown out):
  Stage 1: SHA-256 of the original bytes; open with PyMuPDF; if the file
    cannot be opened, try one Ghostscript repair to a temp buffer. The
    original SHA-256 is always the one recorded; repair_attempted is noted.
  Stage 2: Native extraction per page. Tier 1 is firecrawl-anydoc on a
    single-page PDF (ocr='reject', never hosted). If anydoc is not
    installed or fails on a page, PyMuPDF text is the fallback and the
    fallback is recorded in warnings. Per-page density audit: a page with
    fewer than 30 alphanumeric characters AND raster images present is
    flagged NEEDS_OCR, as is any page where anydoc raises NeedsOcrError.
  Stage 3: NEEDS_OCR pages only are rasterized at 300 DPI and OCRed.
    RapidOCR (PP-OCRv5 ONNX) is tried first, Tesseract (eng, plus hin
    when its traineddata is installed) second. Text is never invented:
    a page that yields nothing is emitted as its anchor plus
    `<!-- OCR_EMPTY_PAGE -->` and recorded.
  Stage 4: verifier.verify_markdown runs on the finished document.
  Stage 5: YAML frontmatter is prepended; md_sha256 is the SHA-256 of
    the Markdown body only (everything after the frontmatter).

No network calls. No PDF is ever modified. Docling and MinerU are not
used. All heavy imports are lazy, inside functions, so this module is
importable without the OCR stack.
"""

import hashlib
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

from .verifier import verify_markdown

HF_DATASET = "imsovikde/rbi-regulatory-archive-1991-2026"
HF_BASE = "https://huggingface.co/datasets/" + HF_DATASET + "/resolve/main/"
DENSITY_MIN_ALNUM = 30
OCR_DPI = 300

_RAPIDOCR_ENGINE = None
_RAPIDOCR_TRIED = False
_TESS_LANGS = None


def _yaml_str(value):
    """Double-quoted YAML scalar, safe for headlines with quotes/colons."""
    if value is None:
        return '""'
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    text = text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return '"' + text + '"'


def _sanitize_doc_id(category, year, document_id):
    raw = "%s_%s_%s" % (category or "UNKNOWN", year or "NA", document_id or "NO_ID")
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "UNKNOWN"


def _load_pymupdf():
    try:
        import pymupdf
        return pymupdf
    except ImportError:
        import fitz
        return fitz


def _try_anydoc_page(page_bytes):
    """Return (markdown_or_None, needs_ocr_bool, error_or_None)."""
    try:
        import anydoc
    except ImportError:
        return None, False, "anydoc not installed"
    try:
        md = anydoc.to_markdown_bytes(page_bytes, ocr="reject")
        return md, False, None
    except Exception as exc:
        name = type(exc).__name__
        if name == "NeedsOcrError":
            return None, True, None
        return None, False, "anydoc %s: %s" % (name, exc)


def _page_to_pdf_bytes(doc, page_index, pymupdf):
    single = pymupdf.open()
    try:
        single.insert_pdf(doc, from_page=page_index, to_page=page_index)
        return single.tobytes()
    finally:
        single.close()


def _pymupdf_page_markdown(text):
    """Plain-text fallback: blank-line separated paragraphs, no invention."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    paras = []
    buf = []
    for ln in lines:
        if ln.strip():
            buf.append(ln.strip())
        elif buf:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return "\n\n".join(paras)


def _rapidocr_lines(png_bytes, warnings):
    """OCR one PNG with RapidOCR. Returns list[str] or None on failure."""
    global _RAPIDOCR_ENGINE, _RAPIDOCR_TRIED
    if not _RAPIDOCR_TRIED:
        _RAPIDOCR_TRIED = True
        try:
            from rapidocr_onnxruntime import RapidOCR
            _RAPIDOCR_ENGINE = RapidOCR()
        except Exception as exc:
            warnings.append("RapidOCR unavailable: %s" % (exc,))
            _RAPIDOCR_ENGINE = None
    if _RAPIDOCR_ENGINE is None:
        return None
    try:
        result, _elapsed = _RAPIDOCR_ENGINE(png_bytes)
    except Exception as exc:
        warnings.append("RapidOCR failed on page: %s" % (exc,))
        return None
    if not result:
        return []
    rows = []
    for box, text, _score in result:
        x = float(box[0][0])
        y = float(box[0][1])
        rows.append((round(y / 20), x, text.strip()))
    rows.sort(key=lambda r: (r[0], r[1]))
    return [r[2] for r in rows if r[2]]


def _tesseract_langs():
    global _TESS_LANGS
    if _TESS_LANGS is None:
        _TESS_LANGS = ["eng"]
        try:
            out = subprocess.run(["tesseract", "--list-langs"],
                                 capture_output=True, text=True, timeout=30)
            langs = out.stdout + out.stderr
            if re.search(r"\bhin\b", langs):
                _TESS_LANGS.append("hin")
        except Exception:
            pass
    return _TESS_LANGS


def _tesseract_lines(png_bytes, warnings):
    """OCR one PNG with the tesseract CLI. Returns list[str] or None."""
    if shutil.which("tesseract") is None:
        warnings.append("tesseract binary not found")
        return None
    langs = "+".join(_tesseract_langs())
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(png_bytes)
            tmp_path = tmp.name
        out = subprocess.run(
            ["tesseract", tmp_path, "stdout", "--psm", "6", "-l", langs],
            capture_output=True, text=True, timeout=300)
    except Exception as exc:
        warnings.append("tesseract failed on page: %s" % (exc,))
        return None
    finally:
        try:
            import os
            os.unlink(tmp_path)
        except Exception:
            pass
    if out.returncode != 0:
        warnings.append("tesseract exit %d: %s" % (out.returncode, out.stderr[:200]))
        return None
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


def _ocr_page_markdown(page, pymupdf, warnings, page_number):
    """Rasterize one page at 300 DPI and OCR it. Returns markdown text."""
    pix = page.get_pixmap(dpi=OCR_DPI)
    png_bytes = pix.tobytes("png")
    lines = _rapidocr_lines(png_bytes, warnings)
    engine = "RapidOCR (PP-OCRv5 ONNX)"
    if not lines:
        if lines == []:
            warnings.append("page %d: RapidOCR returned no text, trying Tesseract"
                            % page_number)
        lines = _tesseract_lines(png_bytes, warnings)
        engine = "Tesseract (%s)" % ("+".join(_tesseract_langs()),)
    if lines is None:
        warnings.append("page %d: no OCR engine produced output" % page_number)
        return "", engine
    if not lines:
        return "", engine
    return "\n\n".join(lines), engine


def _gs_repair(pdf_bytes, warnings):
    """Try a Ghostscript repair to a temp file. Returns bytes or None."""
    if shutil.which("gs") is None:
        warnings.append("ghostscript not found, repair skipped")
        return None
    try:
        with tempfile.TemporaryDirectory() as tmp:
            src = tmp + "/input.pdf"
            dst = tmp + "/repaired.pdf"
            with open(src, "wb") as f:
                f.write(pdf_bytes)
            proc = subprocess.run(
                ["gs", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite",
                 "-dPDFSETTINGS=/prepress", "-o", dst, src],
                capture_output=True, text=True, timeout=300)
            if proc.returncode != 0:
                warnings.append("ghostscript repair failed (exit %d)" % proc.returncode)
                return None
            with open(dst, "rb") as f:
                return f.read()
    except Exception as exc:
        warnings.append("ghostscript repair error: %s" % (exc,))
        return None


def _open_pdf(pdf_bytes, warnings):
    """Open PDF bytes with PyMuPDF, repairing once if needed.

    Returns (doc_or_None, repair_attempted_bool).
    """
    pymupdf = _load_pymupdf()
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        if doc.is_encrypted:
            if not doc.authenticate(""):
                warnings.append("encrypted PDF, cannot authenticate")
                doc.close()
                return None, False
        return doc, False
    except Exception as exc:
        warnings.append("open failed (%s), attempting Ghostscript repair" % (exc,))
    repaired = _gs_repair(pdf_bytes, warnings)
    if repaired is None:
        return None, True
    try:
        doc = pymupdf.open(stream=repaired, filetype="pdf")
        return doc, True
    except Exception as exc:
        warnings.append("open failed after repair: %s" % (exc,))
        return None, True


def convert_pdf(pdf_bytes, meta):
    """Convert one PDF to Markdown.

    meta keys: category, year, listing_date, headline, document_id,
    listing_url, pdf_url, file_path, file_name, pdf_sha256.

    Returns a dict with keys: markdown, md_sha256, total_pages,
    native_pages, ocr_pages, ocr_page_numbers, engine, verification_status,
    warnings, plus repair_attempted, pdf_sha256, page_status.
    """
    warnings = []
    pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()
    if meta.get("pdf_sha256") and meta["pdf_sha256"] != pdf_sha256:
        warnings.append("supplied pdf_sha256 does not match computed hash")
    try:
        pymupdf = _load_pymupdf()
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required: %s" % (exc,))

    doc, repair_attempted = _open_pdf(pdf_bytes, warnings)
    title = (meta.get("headline") or "").strip()
    if not title:
        title = (meta.get("file_name") or "Untitled").rsplit(".pdf", 1)[0]
    doc_id = _sanitize_doc_id(meta.get("category"), meta.get("year"),
                              meta.get("document_id"))
    engine_parts = []
    verification_status = "FAILED_UNREADABLE"
    page_status = []
    total_pages = 0
    native_pages = 0
    ocr_pages = 0
    ocr_page_numbers = []
    body_pages = []

    if doc is None:
        total_pages = 0
    else:
        total_pages = doc.page_count
        try:
            from importlib.metadata import version as _pkg_version
            anydoc_ver = _pkg_version("firecrawl-anydoc")
        except Exception:
            anydoc_ver = "?"
        try:
            import anydoc as _anydoc_mod  # noqa: F401
            engine_parts.append("firecrawl-anydoc %s" % anydoc_ver)
            anydoc_available = True
        except ImportError:
            anydoc_available = False
            warnings.append("anydoc not installed, PyMuPDF text fallback in use")
        for idx in range(total_pages):
            page_number = idx + 1
            page = doc[idx]
            text = page.get_text()
            alnum = len(re.findall(r"[A-Za-z0-9]", text))
            has_images = len(page.get_images()) > 0
            needs_ocr = alnum < DENSITY_MIN_ALNUM and has_images
            status = "native"
            page_md = ""
            if not needs_ocr and anydoc_available:
                page_bytes = _page_to_pdf_bytes(doc, idx, pymupdf)
                page_md, raised_ocr, err = _try_anydoc_page(page_bytes)
                if raised_ocr:
                    needs_ocr = True
                    status = "ocr"
                elif page_md is None:
                    warnings.append("page %d: %s, PyMuPDF fallback" % (page_number, err))
                    page_md = _pymupdf_page_markdown(text)
            elif not needs_ocr:
                page_md = _pymupdf_page_markdown(text)
            if needs_ocr:
                status = "ocr"
                page_md, ocr_engine = _ocr_page_markdown(page, pymupdf, warnings, page_number)
                ocr_name = ocr_engine.split(" (")[0]
                if ocr_name == "RapidOCR":
                    if "RapidOCR (PP-OCRv5 ONNX)" not in engine_parts:
                        engine_parts.append("RapidOCR (PP-OCRv5 ONNX)")
                elif ocr_name == "Tesseract":
                    tess_entry = "Tesseract (%s)" % ("+".join(_tesseract_langs()),)
                    if tess_entry not in engine_parts:
                        engine_parts.append(tess_entry)
                ocr_pages += 1
                ocr_page_numbers.append(page_number)
            else:
                native_pages += 1
            if page_md is None:
                page_md = ""
            if page_md == "" and alnum >= DENSITY_MIN_ALNUM:
                warnings.append("page %d: anydoc returned empty text, PyMuPDF fallback"
                                % page_number)
                page_md = _pymupdf_page_markdown(text)
            page_md = page_md.strip()
            if not page_md:
                page_md = "<!-- OCR_EMPTY_PAGE -->"
                warnings.append("page %d produced no text" % page_number)
            page_status.append({
                "page": page_number,
                "status": status,
                "alnum_chars": alnum,
                "has_images": has_images,
            })
            body_pages.append("<!-- PAGE %d -->\n\n%s" % (page_number, page_md))
        doc.close()

    body = "# %s\n\n%s\n" % (title, "\n\n".join(body_pages)) if body_pages else "# %s\n" % title
    md_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    engine = " + ".join(engine_parts) if engine_parts else "PyMuPDF text"
    if doc is not None and total_pages > 0:
        verification_status = "VERIFIED_LEVEL_5"
    converted_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    frontmatter = "\n".join([
        "---",
        "doc_id: " + _yaml_str(doc_id),
        "title: " + _yaml_str(title),
        "category: " + _yaml_str(meta.get("category") or ""),
        "year: %d" % int(meta.get("year") or 0),
        "source_hf_url: " + _yaml_str(HF_BASE + (meta.get("file_path") or "")),
        "source_rbi_url: " + _yaml_str(meta.get("pdf_url") or ""),
        "pdf_sha256: " + _yaml_str(pdf_sha256),
        "md_sha256: " + _yaml_str(md_sha256),
        "total_pages: %d" % total_pages,
        "native_pages: %d" % native_pages,
        "ocr_pages: %d" % ocr_pages,
        "conversion_engine: " + _yaml_str(engine),
        "converted_at_utc: " + _yaml_str(converted_at),
        "verification_status: " + _yaml_str(verification_status),
        "---",
        "",
    ])
    markdown = frontmatter + body

    if doc is not None and total_pages > 0:
        ok, issues = verify_markdown(markdown, total_pages)
        if not ok:
            verification_status = "NEEDS_REVIEW"
            warnings.extend(issues)
            frontmatter = frontmatter.replace(
                'verification_status: "VERIFIED_LEVEL_5"',
                'verification_status: "NEEDS_REVIEW"')
            markdown = frontmatter + body

    return {
        "markdown": markdown,
        "md_sha256": md_sha256,
        "total_pages": total_pages,
        "native_pages": native_pages,
        "ocr_pages": ocr_pages,
        "ocr_page_numbers": ocr_page_numbers,
        "engine": engine,
        "verification_status": verification_status,
        "warnings": warnings,
        "repair_attempted": repair_attempted,
        "pdf_sha256": pdf_sha256,
        "page_status": page_status,
    }
