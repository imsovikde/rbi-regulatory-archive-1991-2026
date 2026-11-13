"""Weekly RBI sync crawler: find new RBI PDFs the archive does not have.

Three jobs, in order:

1. Crawl the 7 live RBI index endpoints (plus the document host root) and
   collect every PDF link that stays on ``rbi.org.in`` or
   ``rbidocs.rbi.org.in``.
2. Reconcile the discovered URLs against ``manifest/pdf_final_direct_urls.txt``
   and the conversion ledger, returning only genuinely new PDFs.
3. Download a new PDF, verify it is a real PDF, compute its SHA-256, and
   derive its canonical file name. Optionally upload it to Hugging Face,
   but only when ``HF_TOKEN`` is set in the environment.

HTML parsing uses only the standard library (``html.parser``); there is no
BeautifulSoup dependency. HTTP uses ``httpx`` (lazy import) with
exponential backoff and jitter on 429 / 5xx.

No uploads happen unless ``HF_TOKEN`` is set. When it is not set,
``sync_new_to_hf`` returns the new PDFs with ``hf_uploaded=False`` and a
warning string, and the caller must not treat them as synced.
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
    "discover_new",
    "download_new_pdf",
    "extract_document_id",
    "fetch_listing_headline",
    "guess_category",
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

# URL path fragments -> HF folder name. Heuristic only: a new RBI PDF whose
# path matches none of these falls back to "Circulars" and is flagged for
# human review by the caller (see guess_category).
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

_DATE_ON_PAGE_RE = re.compile(
    r"\b(\d{1,2})\s+"
    r"(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(\d{4})\b",
    re.IGNORECASE,
)
# Month-first form, as RBI also writes it: "September 6, 2002".
_DATE_ON_PAGE_RE_MD = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b",
    re.IGNORECASE,
)
_ISO_DATE_RE = re.compile(r"\b(19|20)\d{2}-\d{2}-\d{2}\b")


class CrawlError(Exception):
    """Fetching or parsing an RBI page failed after retries."""


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _http_get(url, timeout=60, retries=4):
    """GET with exponential backoff + jitter on 429 / 5xx / transport errors.

    Returns the response object. Raises CrawlError after the last retry.
    """
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "httpx is not installed; run: pip install httpx"
        ) from exc
    last_error = None
    for attempt in range(retries + 1):
        try:
            from .hf_enumerator import _http_client

            with _http_client(timeout, {"User-Agent": USER_AGENT}) as client:
                response = client.get(url)
        except Exception as exc:
            last_error = CrawlError(f"GET {url} transport error: {exc}")
            if attempt < retries:
                time.sleep(min(60.0, 2.0 ** attempt) * (0.5 + 0.5 * random.random()))
                continue
            raise last_error from exc
        status = response.status_code
        if status in (429, 500, 502, 503, 504):
            last_error = CrawlError(f"GET {url} returned HTTP {status}")
            if attempt < retries:
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(min(60.0, float(retry_after)))
                else:
                    time.sleep(min(60.0, 2.0 ** attempt))
                continue
            raise last_error
        if status != 200:
            raise CrawlError(f"GET {url} returned HTTP {status}")
        return response
    raise last_error  # pragma: no cover


def _rand():
    import random

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


def _is_rbi_pdf_url(url):
    """True when the URL is a PDF on an RBI host."""
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    if host not in _ALLOWED_HOSTS:
        return False
    path = unquote(parsed.path or "")
    return path.lower().endswith(".pdf")


def crawl_index(url, timeout=60, retries=4):
    """Fetch one RBI index page and return its sorted RBI PDF links.

    Only links staying on rbi.org.in / rbidocs.rbi.org.in and ending in
    .pdf are returned. Duplicates are removed.
    """
    response = _http_get(url, timeout=timeout, retries=retries)
    parser = _LinkParser(url)
    parser.feed(response.text)
    found = {link for link in parser.links if _is_rbi_pdf_url(link)}
    return sorted(found)


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


def discover_new(pdf_urls_file, ledger_path, endpoints=None, timeout=60):
    """Crawl live RBI indexes and return PDFs the archive does not have.

    A discovered URL is "new" when it is absent from both
    ``pdf_urls_file`` (the canonical direct-URL list) and the conversion
    ledger. Each returned dict has keys: pdf_url, category,
    category_confident, discovered_at (UTC, ISO-8601). The list is sorted
    by pdf_url for determinism.
    """
    known = _read_known_urls(pdf_urls_file)
    ledger = _read_ledger_urls(ledger_path)
    endpoints = endpoints or RBI_INDEX_ENDPOINTS
    discovered = set()
    for _name, url in endpoints.items():
        discovered.update(crawl_index(url, timeout=timeout))
    new = []
    for pdf_url in sorted(discovered):
        if pdf_url in known:
            continue
        if ledger.get(pdf_url) == "DONE":
            continue
        folder, confident = guess_category(pdf_url)
        new.append({
            "pdf_url": pdf_url,
            "category": folder,
            "category_confident": confident,
            "discovered_at": _utcnow_iso(),
        })
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

    Prefers the ``Id=`` query parameter of the listing URL, else the PDF
    file stem without its extension, else "NO_ID_AS_LISTED".
    """
    if listing_url:
        query = urlparse(listing_url).query
        for part in query.split("&"):
            if part.lower().startswith("id=") and len(part) > 3:
                return unquote(part[3:])
    stem = unquote(urlparse(pdf_url).path.rsplit("/", 1)[-1])
    if stem.lower().endswith(".pdf"):
        stem = stem[:-4]
    return stem or "NO_ID_AS_LISTED"


def _sanitize_filename_part(text):
    """Make one file-name part safe: no slashes, no control characters."""
    cleaned = re.sub(r'[\\/:*?"<>|\r\n\t]+', "-", text or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or "NO_HEADLINE"


def canonical_filename(category, document_id, headline, date_str,
                       date_source="page"):
    """Build ``YYYY-MM-DD_[Category]_[Document-ID]_[Headline-Exact].pdf``.

    ``date_str`` must already be ISO (YYYY-MM-DD). ``date_source`` is
    "page" when the date came from page 1 of the PDF, or "listing" when it
    fell back to the listing date; the caller records it in the ledger.
    """
    head = _sanitize_filename_part(headline) if headline else "NO_HEADLINE"
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
    SHA-256. Raises CrawlError otherwise. The file is written to
    ``dest_dir`` under its URL basename; the caller renames it to the
    canonical name after deriving the headline and date.
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
                          listing_date=None, page_text="", category=None):
    """Derive the canonical file name and date source for a new PDF.

    ``headline`` overrides the fetched listing title when given.
    ``listing_date`` must be ISO (YYYY-MM-DD) when given. The date is
    taken from page 1 text when found, else the listing date, else today.
    ``category`` overrides the folder guessed from the PDF URL (the
    caller passes the crawler's classification, which saw the RBI URL).
    Returns a dict with keys: file_name, date, date_source, document_id,
    headline.
    """
    if headline is None and listing_url:
        headline, _text = fetch_listing_headline(listing_url)
    headline = (headline or "").strip()
    date = _date_from_page_text(page_text)
    date_source = "page"
    if not date:
        date = (listing_date or "").strip()
        date_source = "listing"
    if not date or not _ISO_DATE_RE.fullmatch(date):
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        date_source = "today-fallback"
    document_id = extract_document_id(pdf_url, listing_url)
    folder = category or guess_category(pdf_url)[0]
    file_name = canonical_filename(
        folder, document_id, headline, date, date_source=date_source
    )
    return {
        "file_name": file_name,
        "date": date,
        "date_source": date_source,
        "document_id": document_id,
        "headline": headline or "NO_HEADLINE",
        "category": folder,
    }


def sync_new_to_hf(new_pdfs, repo_id=DATASET_REPO, token=None):
    """Upload new PDFs to the HF dataset when a token is available.

    ``new_pdfs`` is a list of dicts with keys pdf_url, local_path and
    file_name (plus category). When ``HF_TOKEN`` is set in the
    environment (or ``token`` is passed), each PDF is uploaded with
    ``huggingface_hub`` ``create_commit`` and the returned dicts gain
    ``hf_uploaded=True`` and ``hf_path``. When no token is available,
    nothing is uploaded; the returned dicts carry ``hf_uploaded=False``
    and a ``warning`` string, and the caller must treat them as unsynced.

    Returns (uploaded_or_pending_list, warning_or_None).
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
        from huggingface_hub import HfApi
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "huggingface_hub is not installed; run: pip install "
            "huggingface_hub"
        ) from exc
    api = HfApi(token=token)
    try:
        from huggingface_hub import CommitOperationAdd
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "huggingface_hub is not installed; run: pip install "
            "huggingface_hub"
        ) from exc
    operations = []
    for item in new_pdfs:
        hf_path = (
            f"{item['category']}/{item['file_name'][:4]}/{item['file_name']}"
        )
        operations.append(CommitOperationAdd(
            path_in_repo=hf_path, path_or_fileobj=item["local_path"],
        ))
    api.create_commit(
        repo_id,
        operations=operations,
        commit_message=(
            f"Add {len(new_pdfs)} new RBI PDFs discovered by weekly sync"
        ),
        repo_type="dataset",
    )
    return (
        [dict(item, hf_uploaded=True,
              hf_path=f"{item['category']}/{item['file_name'][:4]}/"
              f"{item['file_name']}") for item in new_pdfs],
        None,
    )


def main(argv=None):
    """CLI: discover new RBI PDFs and write them as JSON.

    Usage: python3 -m src.rbi_pipeline.rbi_crawler --urls
    manifest/pdf_final_direct_urls.txt --ledger
    manifest/sha256_conversion_ledger.csv --out new_pdfs.json
    """
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--urls", required=True,
                        help="path to pdf_final_direct_urls.txt")
    parser.add_argument("--ledger", default=None,
                        help="path to sha256_conversion_ledger.csv")
    parser.add_argument("--out", default="new_pdfs.json",
                        help="output JSON file for discovered PDFs")
    args = parser.parse_args(argv)
    found = discover_new(args.urls, args.ledger)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(found, handle, indent=2, ensure_ascii=False)
    print(f"discovered {len(found)} new PDFs, wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
