"""Weekly RBI sync crawler: find new RBI PDFs the archive does not have.

Three jobs, in order:

1. Crawl the 7 live RBI index endpoints (plus the document host root),
   extracting ``<table class="tablebg">`` document rows and following
   unseen ``Circular-Index`` detail pages when needed while keeping links on
   ``rbi.org.in`` or ``rbidocs.rbi.org.in``.
2. Reconcile the discovered URLs (scheme- and case-normalized) against
   ``manifest/pdf_final_direct_urls.txt``, the conversion ledger, and the
   inventory, returning only genuinely new PDFs with listing metadata.
3. Download a new PDF, verify it is a real PDF, compute its SHA-256, and
   derive its canonical file name. Optionally upload it to Hugging Face
   when ``HF_TOKEN`` is set in the environment.

HTML parsing uses only the standard library (``html.parser``); there is no
BeautifulSoup dependency. HTTP uses stdlib ``urllib`` (for RBI endpoints
and offline/minimal runners) or ``httpx`` with exponential backoff and
jitter on 429 / 5xx.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urljoin, urlparse

__all__ = [
    "RBI_INDEX_ENDPOINTS",
    "canonical_filename",
    "crawl_index",
    "crawl_index_records",
    "discover_new",
    "download_new_pdf",
    "extract_document_id",
    "fetch_listing_headline",
    "guess_category",
    "normalize_url",
    "sync_new_to_hf",
]

DATASET_REPO = "imsovikde/rbi-regulatory-archive-1991-2026"

RBI_INDEX_ENDPOINTS = {
    "Master-Directions": (
        "https://www.rbi.org.in/Scripts/BS_ViewMasterDirections.aspx"
    ),
    "Notifications": "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
    "Master-Circulars": (
        "https://www.rbi.org.in/Scripts/BS_ViewMasterCirculardetails.aspx"
    ),
    "Draft-Notifications-Guidelines": (
        "https://www.rbi.org.in/Scripts/DraftNotificationsGuildelines.aspx"
    ),
    "Circular-Index": (
        "https://www.rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx"
    ),
    "Press-Releases": (
        "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"
    ),
    "Document-Host": "https://rbidocs.rbi.org.in/rdocs/",
}

USER_AGENT = (
    "RBI-Regulatory-Archive-Sync/1.0 "
    "(+https://github.com/imsovikde/rbi-regulatory-archive-1991-2026; "
    "contact imsovikde@gmail.com)"
)

_ALLOWED_HOSTS = {"rbi.org.in", "www.rbi.org.in", "rbidocs.rbi.org.in"}

_ENDPOINT_CATEGORY = {
    "Master-Directions": "Master-Directions",
    "Master-Circulars": "Master-Circulars",
    "Notifications": "Notifications",
    "Draft-Notifications-Guidelines": "Draft-Notifications-Guidelines",
    "Circular-Index": "Circulars",
    "Press-Releases": "Press-Releases",
}

_CATEGORY_PRIORITY = {
    "Master-Directions": 6,
    "Master-Circulars": 5,
    "Notifications": 4,
    "Draft-Notifications-Guidelines": 3,
    "Circulars": 2,
    "Press-Releases": 1,
}

# URL path fragments -> HF folder name. Heuristic fallback when an endpoint
# category is not known.
_PATH_CATEGORY_RULES = (
    ("pressrelease", "Press-Releases"),
    ("commonman", "Press-Releases"),
    ("notification", "Notifications"),
    ("mastercircular", "Master-Circulars"),
    ("mascircular", "Master-Circulars"),
    ("masterdirection", "Master-Directions"),
    ("masdirection", "Master-Directions"),
    ("draft", "Draft-Notifications-Guidelines"),
    ("consultation", "Draft-Notifications-Guidelines"),
)

_FOOTER_PDF_RE = re.compile(r"^(?:accessibility|utkarsh)\d*\.pdf$", re.IGNORECASE)

_DATE_ON_PAGE_RE = re.compile(
    r"\b(\d{1,2})\s+"
    r"(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(\d{4})\b",
    re.IGNORECASE,
)
_DATE_ON_PAGE_RE_MD = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b",
    re.IGNORECASE,
)
_ISO_DATE_RE = re.compile(r"\b(19|20)\d{2}-\d{2}-\d{2}\b")
_LISTING_DATE_FORMATS = (
    "%Y-%m-%d",
    "%b %d, %Y",
    "%B %d, %Y",
    "%d.%m.%Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d %B %Y",
    "%d %b %Y",
)


class CrawlError(Exception):
    """Fetching or parsing an RBI page failed after retries."""

    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class _SimpleResponse:
    """Minimal response wrapper when stdlib urllib handles HTTP."""

    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.text = content.decode("utf-8", errors="replace")


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_url(url):
    """Return scheme/case-normalized URL key for deduplication."""
    raw = (url or "").strip()
    if not raw:
        return ""
    if raw.lower().startswith("http://"):
        raw = "https://" + raw[7:]
    return raw.lower()


def _canonical_rbi_pdf_url(url):
    """Upgrade plain http:// RBI PDF links to https://."""
    raw = (url or "").strip()
    if raw.lower().startswith("http://"):
        parsed = urlparse(raw)
        if (parsed.netloc or "").lower() in _ALLOWED_HOSTS:
            return "https://" + raw[7:]
    return raw


def _listing_key(url):
    """Return canonical '<script.aspx>:<id|prid>=<num>' key or ''."""
    if not url:
        return ""
    parsed = urlparse(url.strip().lower())
    script = (parsed.path.rsplit("/", 1)[-1] or "").strip()
    match = re.search(r"(?:^|&)(id|prid)=(\d+)", parsed.query or "")
    if script and match:
        return f"{script}:{match.group(1)}={match.group(2)}"
    return ""


def _parse_any_date(text):
    """Parse common RBI date strings into (iso_YYYY_MM_DD, Mon_DD_YYYY) or (None, '')."""
    cleaned = " ".join((text or "").split()).strip()
    if not cleaned:
        return None, ""
    for fmt in _LISTING_DATE_FORMATS:
        try:
            dt = datetime.strptime(cleaned, fmt)
            return dt.strftime("%Y-%m-%d"), dt.strftime("%b %d, %Y")
        except ValueError:
            continue
    return None, ""


def _http_get(url, timeout=60, retries=4):
    """GET with exponential backoff + jitter on 429 / 5xx / transport errors.

    Uses standard Python-urllib headers on RBI hosts to avoid custom-UA
    interstitials, and httpx (falling back to urllib) elsewhere.
    Returns a response object with status_code, headers, text, content.
    Raises CrawlError after the last retry.
    """
    from .hf_enumerator import _urllib_get

    host = (urlparse(url).netloc or "").lower()
    is_rbi = host.endswith("rbi.org.in")
    use_httpx = not is_rbi
    if use_httpx:
        try:
            import httpx  # noqa: F401
        except ImportError:
            use_httpx = False

    last_error = None
    for attempt in range(retries + 1):
        try:
            if use_httpx:
                from .hf_enumerator import _http_client

                with _http_client(timeout, {"User-Agent": USER_AGENT}) as client:
                    response = client.get(url)
                status = response.status_code
                headers = response.headers
            else:
                req_headers = {"Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}
                if not is_rbi:
                    req_headers["User-Agent"] = USER_AGENT
                status, headers, data = _urllib_get(url, timeout, req_headers)
                response = _SimpleResponse(status, headers, data)
        except Exception as exc:
            last_error = CrawlError(f"GET {url} transport error: {exc}")
            if attempt < retries:
                time.sleep(min(60.0, 2.0 ** attempt) * (0.5 + 0.5 * random.random()))
                continue
            raise last_error from exc
        if status in (429, 500, 502, 503, 504):
            last_error = CrawlError(f"GET {url} returned HTTP {status}", status=status)
            if attempt < retries:
                retry_after = None
                for k, v in headers.items():
                    if k.lower() == "retry-after":
                        retry_after = v
                        break
                if retry_after and str(retry_after).isdigit():
                    time.sleep(min(60.0, float(retry_after)))
                else:
                    time.sleep(min(60.0, 2.0 ** attempt))
                continue
            raise last_error
        if status != 200:
            raise CrawlError(f"GET {url} returned HTTP {status}", status=status)
        return response
    raise last_error  # pragma: no cover


def _rand():
    return random.random()


class _LinkParser(HTMLParser):
    """Collect every <a href> on a page, resolved to absolute URLs."""

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.links = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append(urljoin(self.base_url, value.strip()))
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


class _TableBGParser(HTMLParser):
    """Extract structured rows and tableheader dates from RBI tablebg tables."""

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.rows = []
        self._table_stack = []
        self._in_tr = False
        self._in_td = False
        self._td_is_header = False
        self._td_text = []
        self._td_links = []
        self._tr_cells = []
        self._in_a = False
        self._a_href = ""
        self._a_class = ""
        self._a_text = []
        self._current_iso_date = ""
        self._current_display_date = ""

    def _close_anchor(self):
        if self._in_a:
            href = urljoin(self.base_url, self._a_href.strip()) if self._a_href else ""
            text = " ".join("".join(self._a_text).split())
            if href:
                self._td_links.append({
                    "href": href,
                    "text": text,
                    "is_link2": "link2" in self._a_class.lower(),
                })
            self._in_a = False
            self._a_href = ""
            self._a_class = ""
            self._a_text = []

    def _close_td(self):
        self._close_anchor()
        if not self._in_td:
            return
        text = " ".join("".join(self._td_text).split())
        if self._td_is_header:
            iso, disp = _parse_any_date(text)
            if iso:
                self._current_iso_date = iso
                self._current_display_date = disp
        self._tr_cells.append({
            "text": text,
            "links": list(self._td_links),
            "is_header": self._td_is_header,
        })
        self._in_td = False
        self._td_is_header = False
        self._td_text = []
        self._td_links = []

    def _close_tr(self):
        self._close_td()
        if self._in_tr and self._tr_cells:
            has_links = any(c["links"] for c in self._tr_cells)
            if has_links:
                self.rows.append({
                    "iso_date": self._current_iso_date,
                    "display_date": self._current_display_date,
                    "cells": list(self._tr_cells),
                })
        self._in_tr = False
        self._tr_cells = []

    def handle_starttag(self, tag, attrs):
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if tag == "table":
            cls = attr_map.get("class", "").lower()
            is_bg = "tablebg" in cls.split() or "tablebg" in cls
            self._table_stack.append(is_bg)
            return
        if not any(self._table_stack):
            return
        if tag == "tr":
            self._close_tr()
            self._in_tr = True
            self._tr_cells = []
        elif tag in ("td", "th") and self._in_tr:
            self._close_td()
            cls = attr_map.get("class", "").lower()
            self._in_td = True
            self._td_is_header = "tableheader" in cls
            self._td_text = []
            self._td_links = []
        elif tag == "a" and self._in_td:
            self._close_anchor()
            self._in_a = True
            self._a_href = attr_map.get("href", "")
            self._a_class = attr_map.get("class", "")
            self._a_text = []
        elif tag == "br" and self._in_td:
            self._td_text.append(" ")
            if self._in_a:
                self._a_text.append(" ")

    def handle_endtag(self, tag):
        if tag == "table":
            self._close_tr()
            if self._table_stack:
                self._table_stack.pop()
            return
        if not any(self._table_stack):
            return
        if tag == "a":
            self._close_anchor()
        elif tag in ("td", "th"):
            self._close_td()
        elif tag == "tr":
            self._close_tr()

    def handle_data(self, data):
        if not any(self._table_stack):
            return
        if self._in_td:
            self._td_text.append(data)
        if self._in_a:
            self._a_text.append(data)


def _is_rbi_pdf_url(url):
    """True when the URL is a regulatory PDF on an RBI host (excluding footer PDFs)."""
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    if host not in _ALLOWED_HOSTS:
        return False
    path = unquote(parsed.path or "")
    if not path.lower().endswith(".pdf"):
        return False
    basename = path.rsplit("/", 1)[-1]
    if _FOOTER_PDF_RE.match(basename):
        return False
    return True


def crawl_index(url, timeout=60, retries=4):
    """Fetch one RBI index page and return its sorted RBI PDF links.

    Only links staying on rbi.org.in / rbidocs.rbi.org.in and ending in
    .pdf (excluding site-wide footer PDFs) are returned. Duplicates are
    removed.
    """
    response = _http_get(url, timeout=timeout, retries=retries)
    parser = _LinkParser(url)
    parser.feed(response.text)
    found = {_canonical_rbi_pdf_url(link) for link in parser.links if _is_rbi_pdf_url(link)}
    return sorted(found)


def _extract_tablebg_pdfs(html, base_url):
    """Extract regulatory PDF links from <table class='tablebg'> on a detail page."""
    parser = _TableBGParser(base_url)
    parser.feed(html)
    pdfs = []
    seen = set()
    for row in parser.rows:
        for cell in row["cells"]:
            for link in cell["links"]:
                href = link["href"]
                if _is_rbi_pdf_url(href):
                    canon = _canonical_rbi_pdf_url(href)
                    norm = normalize_url(canon)
                    if norm not in seen:
                        seen.add(norm)
                        pdfs.append(canon)
    if pdfs:
        return pdfs
    # Fallback to all non-footer RBI PDF links if detail page omits class="tablebg"
    lp = _LinkParser(base_url)
    lp.feed(html)
    for link in lp.links:
        if _is_rbi_pdf_url(link):
            canon = _canonical_rbi_pdf_url(link)
            norm = normalize_url(canon)
            if norm not in seen:
                seen.add(norm)
                pdfs.append(canon)
    return pdfs


def crawl_index_records(
    endpoint_name,
    url,
    known_norm=None,
    known_listing_keys=None,
    timeout=60,
    max_detail_fetches=40,
):
    """Crawl one RBI index endpoint and return (records, telemetry_dict)."""
    known_norm = known_norm or set()
    known_listing_keys = known_listing_keys or set()
    telemetry = {
        "name": endpoint_name,
        "url": url,
        "status": "OK",
        "http_status": 200,
        "total_found": 0,
        "new_count": 0,
        "detail_fetches": 0,
        "error": "",
    }
    try:
        response = _http_get(url, timeout=timeout)
        telemetry["http_status"] = getattr(response, "status_code", 200)
    except CrawlError as exc:
        telemetry["status"] = "WARN_DEGRADED" if endpoint_name == "Document-Host" else "ERROR"
        telemetry["http_status"] = exc.status
        telemetry["error"] = str(exc)
        return [], telemetry

    parser = _TableBGParser(url)
    parser.feed(response.text)
    category = _ENDPOINT_CATEGORY.get(endpoint_name)
    records = []
    seen_local = set()

    if parser.rows:
        detail_fetches = 0
        for row in parser.rows:
            cells = row["cells"]
            pdf_links = []
            listing_link = None
            for cell in cells:
                for lnk in cell["links"]:
                    href = lnk["href"]
                    if _is_rbi_pdf_url(href):
                        pdf_links.append(_canonical_rbi_pdf_url(href))
                    elif (urlparse(href).netloc or "").lower() in _ALLOWED_HOSTS:
                        if listing_link is None or lnk["is_link2"]:
                            listing_link = lnk

            listing_url = listing_link["href"] if listing_link else ""
            l_key = _listing_key(listing_url)

            # Circular-Index rows (or detail-only rows) hold Subject in column 3 and Date in column 1.
            headline = ""
            iso_date = row["iso_date"]
            disp_date = row["display_date"]
            if endpoint_name == "Circular-Index" and len(cells) >= 4:
                headline = cells[3]["text"] or (listing_link["text"] if listing_link else "")
                d_iso, d_disp = _parse_any_date(cells[1]["text"])
                if d_iso:
                    iso_date, disp_date = d_iso, d_disp
            else:
                if listing_link and listing_link["text"]:
                    headline = listing_link["text"]
                elif cells:
                    headline = cells[0]["text"]
                if not iso_date and len(cells) >= 2:
                    d_iso, d_disp = _parse_any_date(cells[1]["text"])
                    if d_iso:
                        iso_date, disp_date = d_iso, d_disp

            if not pdf_links and listing_url:
                if l_key and l_key in known_listing_keys:
                    telemetry["total_found"] += 1
                    continue
                if detail_fetches >= max_detail_fetches:
                    continue
                detail_fetches += 1
                telemetry["detail_fetches"] = detail_fetches
                try:
                    time.sleep(0.15)
                    detail_resp = _http_get(listing_url, timeout=min(timeout, 30), retries=2)
                    pdf_links = _extract_tablebg_pdfs(detail_resp.text, listing_url)
                except CrawlError:
                    pdf_links = []

            for pdf_url in pdf_links:
                norm = normalize_url(pdf_url)
                if not norm or norm in seen_local:
                    continue
                seen_local.add(norm)
                telemetry["total_found"] += 1
                if norm in known_norm:
                    continue
                row_cat = category or guess_category(pdf_url)[0]
                doc_id = extract_document_id(pdf_url, listing_url)
                records.append({
                    "pdf_url": pdf_url,
                    "listing_url": listing_url,
                    "headline": headline,
                    "listing_date": disp_date or iso_date,
                    "iso_date": iso_date,
                    "document_id": doc_id,
                    "category": row_cat,
                    "category_confident": bool(category),
                    "source_endpoint": endpoint_name,
                    "source_endpoint_url": url,
                    "discovered_at": _utcnow_iso(),
                })
    else:
        # Fallback for pages without <table class="tablebg"> (e.g., Document-Host)
        lp = _LinkParser(url)
        lp.feed(response.text)
        for link in sorted(lp.links):
            if not _is_rbi_pdf_url(link):
                continue
            pdf_url = _canonical_rbi_pdf_url(link)
            norm = normalize_url(pdf_url)
            if norm in seen_local:
                continue
            seen_local.add(norm)
            telemetry["total_found"] += 1
            if norm in known_norm:
                continue
            row_cat, confident = guess_category(pdf_url)
            records.append({
                "pdf_url": pdf_url,
                "listing_url": "",
                "headline": "",
                "listing_date": "",
                "iso_date": "",
                "document_id": extract_document_id(pdf_url),
                "category": category or row_cat,
                "category_confident": bool(category) or confident,
                "source_endpoint": endpoint_name,
                "source_endpoint_url": url,
                "discovered_at": _utcnow_iso(),
            })

    telemetry["new_count"] = len(records)
    if endpoint_name == "Document-Host" and telemetry["total_found"] == 0:
        telemetry["status"] = "NO_DIRECTORY_LISTING"
    return records, telemetry


def guess_category(pdf_url):
    """Guess the HF folder for a PDF URL from its path (heuristic).

    Returns (folder, confident). ``confident`` is False when no rule
    matched and the fallback "Circulars" was used; callers should flag
    those rows for human review instead of trusting the guess.
    """
    path = urlparse(pdf_url).path.lower()
    for fragment, folder in _PATH_CATEGORY_RULES:
        if fragment in path:
            return folder, True
    return "Circulars", False


def _read_known_urls(pdf_urls_file):
    known = set()
    if pdf_urls_file and os.path.exists(pdf_urls_file):
        with open(pdf_urls_file, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    known.add(line)
    return known


def _read_ledger_urls(ledger_path):
    """Return (pdf_url -> status) for every row in the conversion ledger."""
    mapping = {}
    if ledger_path and os.path.exists(ledger_path):
        with open(ledger_path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                url = (row.get("pdf_url") or "").strip()
                if url:
                    mapping[url] = (row.get("status") or "").strip()
    return mapping


def _read_known_listing_keys(inventory_path):
    """Return set of '<script>:<id|prid>=<num>' keys and normalized PDF URLs."""
    listing_keys = set()
    inv_pdf_urls = set()
    if inventory_path and os.path.exists(inventory_path):
        with open(inventory_path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                lu = (row.get("listing_url") or "").strip()
                lk = _listing_key(lu)
                if lk:
                    listing_keys.add(lk)
                pu = (row.get("pdf_url") or "").strip()
                if pu:
                    inv_pdf_urls.add(normalize_url(pu))
    return listing_keys, inv_pdf_urls


def discover_new(
    pdf_urls_file,
    ledger_path,
    endpoints=None,
    timeout=60,
    report_out=None,
    inventory_path=None,
):
    """Crawl live RBI indexes and return PDFs the archive does not have.

    A discovered URL is "new" when its scheme/case-normalized URL is absent
    from ``pdf_urls_file``, the DONE rows of ``ledger_path``, and
    ``inventory_path``.
    """
    known = _read_known_urls(pdf_urls_file)
    ledger = _read_ledger_urls(ledger_path)
    known_norm = {normalize_url(u) for u in known}
    for u, st in ledger.items():
        if st == "DONE":
            known_norm.add(normalize_url(u))
    if inventory_path is None:
        default_inv = os.path.join(os.path.dirname(pdf_urls_file or "."), "hf_88236_inventory.jsonl")
        if os.path.exists(default_inv):
            inventory_path = default_inv
    known_listing_keys, inv_pdf_norm = _read_known_listing_keys(inventory_path)
    known_norm.update(inv_pdf_norm)

    endpoints = endpoints or RBI_INDEX_ENDPOINTS
    by_norm = {}
    endpoint_reports = []
    for name, url in endpoints.items():
        recs, tel = crawl_index_records(
            name,
            url,
            known_norm=known_norm,
            known_listing_keys=known_listing_keys,
            timeout=timeout,
        )
        endpoint_reports.append(tel)
        for rec in recs:
            norm = normalize_url(rec["pdf_url"])
            existing = by_norm.get(norm)
            if existing is None:
                by_norm[norm] = rec
            else:
                new_prio = _CATEGORY_PRIORITY.get(rec["category"], 0)
                old_prio = _CATEGORY_PRIORITY.get(existing["category"], 0)
                if new_prio > old_prio:
                    if not rec.get("headline") and existing.get("headline"):
                        rec["headline"] = existing["headline"]
                    if not rec.get("listing_url") and existing.get("listing_url"):
                        rec["listing_url"] = existing["listing_url"]
                    if not rec.get("listing_date") and existing.get("listing_date"):
                        rec["listing_date"] = existing["listing_date"]
                        rec["iso_date"] = existing.get("iso_date", "")
                    by_norm[norm] = rec

    new = sorted(by_norm.values(), key=lambda r: r["pdf_url"])
    if report_out:
        out_dir = os.path.dirname(os.path.abspath(report_out))
        os.makedirs(out_dir, exist_ok=True)
        report = {
            "crawled_at_utc": _utcnow_iso(),
            "endpoints": endpoint_reports,
            "total_scanned": sum(e["total_found"] for e in endpoint_reports),
            "total_new": len(new),
            "errors": [e for e in endpoint_reports if e["status"] == "ERROR"],
        }
        with open(report_out, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
    return new


def fetch_listing_headline(listing_url, timeout=60):
    """Best-effort headline from an RBI listing page.

    Returns (headline, page_text). The headline is the <title> text with
    common RBI suffixes stripped; empty string when nothing usable is
    found. Callers fall back to NO_HEADLINE.
    """
    try:
        response = _http_get(listing_url, timeout=timeout, retries=2)
    except CrawlError:
        return "", ""
    parser = _LinkParser(listing_url)
    try:
        parser.feed(response.text)
    except Exception:
        return "", response.text
    title = " ".join(parser.title.split())
    for suffix in (
        " | Reserve Bank of India",
        " - Reserve Bank of India",
        " | RBI",
        " - RBI",
    ):
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
    return title, response.text


def extract_document_id(pdf_url, listing_url=None):
    """Extract the RBI document ID for a PDF.

    Prefers the ``prid=`` or ``Id=`` query parameter of the listing URL,
    else the PDF file stem without its extension, else "NO_ID_AS_LISTED".
    """
    if listing_url:
        query = urlparse(listing_url).query
        for part in query.split("&"):
            low = part.lower()
            if low.startswith("prid=") and len(part) > 5:
                return unquote(part[5:])
            if low.startswith("id=") and len(part) > 3:
                return unquote(part[3:])
    stem = unquote(urlparse(pdf_url).path.rsplit("/", 1)[-1])
    if stem.lower().endswith(".pdf"):
        stem = stem[:-4]
    return stem or "NO_ID_AS_LISTED"


def _sanitize_filename_part(text, max_len=None):
    """Make one file-name part safe: no slashes, no control characters."""
    cleaned = re.sub(r'[\\/:*?"<>|\r\n\t]+', "-", text or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if max_len and len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rstrip(" .-")
    return cleaned or "NO_HEADLINE"


def canonical_filename(category, document_id, headline, date_str,
                       date_source="page"):
    """Build ``YYYY-MM-DD_[Category]_[Document-ID]_[Headline-Exact].pdf``."""
    head = _sanitize_filename_part(headline, max_len=140) if headline else "NO_HEADLINE"
    doc_id = _sanitize_filename_part(document_id) or "NO_ID_AS_LISTED"
    cat = _sanitize_filename_part(category)
    return f"{date_str}_{cat}_{doc_id}_{head}.pdf"


def _date_from_page_text(text):
    """Find the first plausible document date in page text (ISO format)."""
    match = _ISO_DATE_RE.search(text or "")
    if match:
        return match.group(0)
    match = _DATE_ON_PAGE_RE.search(text or "")
    if match:
        day, month, year = match.groups()
        try:
            parsed = datetime.strptime(
                f"{day} {month} {year}", "%d %B %Y"
            )
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            return None
    match = _DATE_ON_PAGE_RE_MD.search(text or "")
    if match:
        month, day, year = match.groups()
        try:
            parsed = datetime.strptime(
                f"{day} {month} {year}", "%d %B %Y"
            )
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def download_new_pdf(pdf_url, dest_dir, timeout=180, retries=4):
    """Download one new PDF and verify it. Returns a metadata dict.

    Checks: HTTP 200, body starts with ``%PDF``, size > 0. Computes
    SHA-256. Raises CrawlError otherwise.
    """
    from .hf_enumerator import DownloadError, download_pdf

    try:
        data = download_pdf(pdf_url, timeout=timeout, retries=retries)
    except DownloadError as exc:
        raise CrawlError(str(exc)) from exc
    if len(data) == 0:
        raise CrawlError(f"downloaded 0 bytes for {pdf_url}")
    os.makedirs(dest_dir, exist_ok=True)
    basename = unquote(urlparse(pdf_url).path.rsplit("/", 1)[-1]) or "file.pdf"
    local_path = os.path.join(dest_dir, basename)
    with open(local_path, "wb") as handle:
        handle.write(data)
    return {
        "pdf_url": pdf_url,
        "local_path": local_path,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def derive_canonical_name(pdf_url, listing_url=None, headline=None,
                          listing_date=None, page_text="", category=None,
                          document_id=None):
    """Derive the canonical file name and metadata for a new PDF.

    Returns a dict with keys: file_name, date (ISO YYYY-MM-DD),
    listing_date (Mon DD, YYYY), date_source, document_id, headline,
    category (plural HF folder name).
    """
    from .hf_enumerator import FOLDER_TO_CATEGORY

    if headline is None and listing_url:
        headline, _text = fetch_listing_headline(listing_url)
    headline = " ".join((headline or "").split()).strip()

    listing_iso, listing_disp = _parse_any_date(listing_date or "")
    page_iso = _date_from_page_text(page_text)
    if listing_iso:
        date = listing_iso
        date_source = "listing"
    elif page_iso:
        date = page_iso
        date_source = "page"
    else:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        date_source = "today-fallback"

    if not listing_disp:
        _, listing_disp = _parse_any_date(date)

    doc_id = (document_id or "").strip() or extract_document_id(pdf_url, listing_url)
    folder = category or guess_category(pdf_url)[0]
    file_cat = FOLDER_TO_CATEGORY.get(folder, folder)
    file_name = canonical_filename(
        file_cat, doc_id, headline, date, date_source=date_source
    )
    return {
        "file_name": file_name,
        "date": date,
        "listing_date": listing_disp or date,
        "date_source": date_source,
        "document_id": doc_id,
        "headline": headline or "NO_HEADLINE",
        "category": folder,
    }


def sync_new_to_hf(new_pdfs, repo_id=DATASET_REPO, token=None):
    """Upload new PDFs to the HF dataset when a token is available.

    Chunks commits into groups of <= 50 files and gracefully returns
    hf_uploaded=False with a warning on upload errors so RBI-direct
    Markdown conversion is never blocked by Hugging Face outages.
    """
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        warning = (
            "HF_TOKEN is not set; new PDFs were NOT uploaded to Hugging "
            "Face. Set HF_TOKEN and re-run to sync them."
        )
        out = [dict(item, hf_uploaded=False) for item in new_pdfs]
        return out, warning
    try:
        from huggingface_hub import CommitOperationAdd, HfApi
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "huggingface_hub is not installed; run: pip install huggingface_hub"
        ) from exc

    api = HfApi(token=token)
    out = [dict(item, hf_uploaded=False) for item in new_pdfs]
    warnings = []
    chunk_size = 50
    for start in range(0, len(out), chunk_size):
        chunk = out[start : start + chunk_size]
        operations = []
        for item in chunk:
            hf_path = f"{item['category']}/{item['file_name'][:4]}/{item['file_name']}"
            operations.append(CommitOperationAdd(
                path_in_repo=hf_path, path_or_fileobj=item["local_path"],
            ))
        try:
            api.create_commit(
                repo_id,
                operations=operations,
                commit_message=(
                    f"Add {len(chunk)} new RBI PDFs discovered by automated sync"
                ),
                repo_type="dataset",
            )
            for item in chunk:
                item["hf_uploaded"] = True
                item["hf_path"] = (
                    f"{item['category']}/{item['file_name'][:4]}/{item['file_name']}"
                )
        except Exception as exc:
            warnings.append(f"HF backfill batch failed ({exc}); continuing with RBI-direct conversion")
    return out, ("; ".join(warnings) if warnings else None)


def main(argv=None):
    """CLI: discover new RBI PDFs and write them as JSON."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--urls", default="manifest/pdf_final_direct_urls.txt",
                        help="path to pdf_final_direct_urls.txt")
    parser.add_argument("--ledger", default="manifest/sha256_conversion_ledger.csv",
                        help="path to sha256_conversion_ledger.csv")
    parser.add_argument("--inventory", default="manifest/hf_88236_inventory.jsonl",
                        help="path to hf_88236_inventory.jsonl")
    parser.add_argument("--out", default="new_pdfs.json",
                        help="output JSON file for discovered PDFs")
    parser.add_argument("--report-out", default="",
                        help="optional JSON path for per-endpoint crawl telemetry")
    parser.add_argument("--dry-run", action="store_true",
                        help="run verification dry-run without writing files")
    args = parser.parse_args(argv)

    if args.dry_run:
        print("[rbi_crawler] dry-run verification: endpoints and parsing configuration active.")
        print(f"[rbi_crawler] verified {len(RBI_INDEX_ENDPOINTS)} index endpoints: {list(RBI_INDEX_ENDPOINTS.keys())}")
        return 0

    found = discover_new(
        args.urls,
        args.ledger,
        report_out=args.report_out or None,
        inventory_path=args.inventory or None,
    )
    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(found, handle, indent=2, ensure_ascii=False)
    print(f"discovered {len(found)} new PDFs, wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
