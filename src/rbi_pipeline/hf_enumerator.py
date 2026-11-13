"""Enumerate the RBI Regulatory Archive dataset.

Two sources of truth, in priority order:

1. A local manifest CSV (preferred). Deterministic, offline, and exactly the
   census that was verified file by file. This is what the conversion runner
   uses. See :func:`iter_inventory`.
2. The public Hugging Face dataset tree, listed with ``huggingface_hub``
   without any token. Used only to verify that the local manifest and the
   remote dataset agree. See :func:`list_repo_files`.

All third-party imports are lazy so that importing this module never fails
on a machine where ``httpx`` / ``huggingface_hub`` are not installed yet.
Only functions that actually need them import them, and they raise a clear
error naming the missing package.

No secrets are read or stored here. HF reads are public and need no token.
"""

from __future__ import annotations

import csv
import hashlib
import os
import random
import time
from datetime import datetime
from urllib.parse import quote

__all__ = [
    "DATASET_REPO",
    "DownloadError",
    "download_pdf",
    "hf_resolve_url",
    "iter_inventory",
    "list_repo_files",
]

DATASET_REPO = "imsovikde/rbi-regulatory-archive-1991-2026"
HF_BASE = "https://huggingface.co/datasets/" + DATASET_REPO

# Manifest category value -> Hugging Face folder name. The manifest stores
# singular category labels ("Press-Release") while the dataset folders are
# plural ("Press-Releases"). The folder is always derived from
# stored_relative_path instead, this map is only a fallback.
CATEGORY_TO_FOLDER = {
    "Master-Direction": "Master-Directions",
    "Notification": "Notifications",
    "Master-Circular": "Master-Circulars",
    "Draft-Notification": "Draft-Notifications-Guidelines",
    "Circular": "Circulars",
    "Press-Release": "Press-Releases",
}

# Rows are ordered by (category, year, listing_date, file_name). Listing
# dates in the manifest look like "September 06, 2002".
_DATE_FORMATS = ("%B %d, %Y", "%B %d %Y", "%Y-%m-%d")


class DownloadError(Exception):
    """A PDF download failed, or the bytes failed verification.

    Attributes: url, status (HTTP status or None), reason (short message).
    """

    def __init__(self, url, reason, status=None):
        super().__init__(f"download failed for {url}: {reason}")
        self.url = url
        self.reason = reason
        self.status = status


def _parse_listing_date(raw):
    """Return a sortable key for a manifest listing_date string.

    Parses "Month DD, YYYY" into a date; unparseable or empty values sort
    after all real dates, ordered by their raw string so the result is
    still deterministic.
    """
    text = (raw or "").strip()
    if not text:
        return (datetime.max.date(), "")
    for fmt in _DATE_FORMATS:
        try:
            return (datetime.strptime(text, fmt).date(), "")
        except ValueError:
            continue
    return (datetime.max.date(), text)


def _inventory_row(raw):
    """Map one raw manifest CSV row to the canonical inventory dict."""
    file_path = (raw.get("stored_relative_path") or "").strip()
    folder = file_path.split("/")[0] if "/" in file_path else ""
    if not folder:
        folder = CATEGORY_TO_FOLDER.get(
            (raw.get("category") or "").strip(), ""
        )
    year_raw = (raw.get("year") or "").strip()
    try:
        year = int(year_raw)
    except (TypeError, ValueError):
        year = 0
    bytes_raw = (raw.get("bytes") or "").strip()
    try:
        size = int(bytes_raw) if bytes_raw else None
    except ValueError:
        size = None
    return {
        "category": (raw.get("category") or "").strip(),
        "folder": folder,
        "year": year,
        "listing_date": (raw.get("listing_date") or "").strip(),
        "headline": (raw.get("headline_exact") or "").strip(),
        "document_id": (raw.get("document_id") or "").strip(),
        "listing_url": (raw.get("listing_page_url") or "").strip(),
        "pdf_url": (raw.get("final_direct_url") or "").strip(),
        "file_path": file_path,
        "file_name": (raw.get("file_name") or "").strip(),
        "bytes": size,
        "sha256": (raw.get("sha256") or "").strip().lower(),
    }


def iter_inventory(manifest_path):
    """Yield DOWNLOADED inventory rows from a manifest CSV, in order.

    Order is deterministic: (category, year, listing_date, file_name).
    Only rows with download_status == "DOWNLOADED" are yielded; BLOCKED
    rows have no PDF and therefore nothing to convert.

    Each yielded dict has keys: category, folder, year, listing_date,
    headline, document_id, listing_url, pdf_url, file_path, file_name,
    bytes, sha256. ``folder`` is the Hugging Face folder name derived from
    stored_relative_path (extra key, not in the brief, because the manifest
    category label differs from the folder name).
    """
    with open(manifest_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for raw in reader:
            if (raw.get("download_status") or "").strip() != "DOWNLOADED":
                continue
            rows.append(_inventory_row(raw))
    rows.sort(
        key=lambda r: (
            r["category"],
            r["year"],
            _parse_listing_date(r["listing_date"]),
            r["file_name"],
        )
    )
    yield from rows


def hf_resolve_url(file_path):
    """Return the public Hugging Face resolve URL for a dataset file path.

    Each path segment is percent-encoded (file names contain spaces), the
    slashes between folders are kept.
    """
    quoted = quote(file_path.strip(), safe="/")
    return f"{HF_BASE}/resolve/main/{quoted}"


def list_repo_files(repo_id=DATASET_REPO, revision="main"):
    """List all file paths in the public HF dataset (verification fallback).

    Uses huggingface_hub with no token. Returns a sorted list of paths.
    Raises RuntimeError with a clear message if huggingface_hub is missing.
    """
    try:
        from huggingface_hub import HfApi
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "huggingface_hub is not installed; run: pip install huggingface_hub"
        ) from exc
    api = HfApi()
    paths = api.list_repo_files(
        repo_id, repo_type="dataset", revision=revision
    )
    return sorted(paths)


def _sleep_backoff(attempt, base=1.0, cap=60.0):
    """Exponential backoff with full jitter, in seconds."""
    delay = min(cap, base * (2 ** attempt))
    time.sleep(random.uniform(0, delay))


def _http_client(timeout, headers):
    """Build an httpx client that works behind proxies httpx cannot parse.

    httpx reads proxy settings from the environment by default, but its
    NO_PROXY parsing fails on bracketed IPv6 entries (for example
    "[::1]") with "InvalidURL: Invalid port". Passing the proxy
    explicitly and disabling trust_env avoids that parse entirely.
    When no proxy variable is set (GitHub Actions runners), proxy is
    None and the client connects directly.
    """
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover - missing dependency
        raise RuntimeError(
            "httpx is not installed; run: pip install httpx"
        ) from exc
    proxy = (
        os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )
    # trust_env=False above also drops SSL_CERT_FILE, which is how
    # this VM points Python at the egress proxy's CA bundle
    # (/run/hatch/egress-tls/ca-bundle.pem). Pass it explicitly so
    # verification stays ON; on plain runners it is unset and the
    # default bundle is used.
    verify = (
        os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
        or True
    )
    return httpx.Client(
        timeout=timeout, follow_redirects=True, headers=headers,
        proxy=proxy, trust_env=False, verify=verify,
    )


def download_pdf(url, timeout=120, retries=4, expected_sha256=None,
                 expected_bytes=None):
    """Download one PDF and verify it. Returns the raw bytes.

    Retries with exponential backoff + jitter on HTTP 429 / 5xx and on
    transport errors. Raises :class:`DownloadError` when:

    - the final status is not 200,
    - the body does not start with the ``%PDF`` magic bytes,
    - ``expected_bytes`` is given and the length differs,
    - ``expected_sha256`` is given and the SHA-256 differs.

    ``retries`` is the number of retries after the first attempt.
    """
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover - missing dependency
        # Already checked by _http_client; kept for a clear error if the
        # helper is ever bypassed.
        raise RuntimeError(
            "httpx is not installed; run: pip install httpx"
        ) from exc

    last_error = None
    for attempt in range(retries + 1):
        try:
            with _http_client(
                timeout, {"User-Agent": "RBI-Regulatory-Archive/1.0"},
            ) as client:
                response = client.get(url)
        except Exception as exc:  # transport error: retry
            last_error = DownloadError(url, f"transport error: {exc}")
            if attempt < retries:
                _sleep_backoff(attempt)
                continue
            raise last_error from exc

        status = response.status_code
        if status in (429, 500, 502, 503, 504):
            last_error = DownloadError(
                url, f"HTTP {status} (retryable)", status=status
            )
            if attempt < retries:
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    time.sleep(min(60.0, float(retry_after)))
                else:
                    _sleep_backoff(attempt)
                continue
            raise last_error
        if status != 200:
            raise DownloadError(url, f"HTTP {status}", status=status)

        data = response.content
        if not data.startswith(b"%PDF"):
            raise DownloadError(
                url, "body does not start with %PDF magic bytes", status=200
            )
        if expected_bytes is not None and len(data) != expected_bytes:
            raise DownloadError(
                url,
                f"byte length {len(data)} != expected {expected_bytes}",
                status=200,
            )
        if expected_sha256:
            digest = hashlib.sha256(data).hexdigest()
            if digest != expected_sha256.lower():
                raise DownloadError(
                    url,
                    f"sha256 {digest} != expected {expected_sha256}",
                    status=200,
                )
        return data

    raise last_error  # pragma: no cover - loop always returns or raises
