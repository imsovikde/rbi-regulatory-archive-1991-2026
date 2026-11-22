"""Unit tests for the RBI archive sync, audit, and intelligent commit pipeline."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest import mock

from src.rbi_pipeline import rbi_crawler
from scripts import audit_parity, generate_sync_commit_message, register_new_documents


PRESS_RELEASE_HTML = """
<html><body>
<table class="tablebg" width="100%">
  <tr><td class="tableheader" colspan="4"><b>Nov 20, 2026<b></td></tr>
  <tr>
    <td><a class='link2' href=BS_PressReleaseDisplay.aspx?prid=64017>Conversion/Switch of State Government Securities</a></td>
    <td><a href='https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR153980EC0AE092E14AE6963872D7C9520E39.PDF'>PDF</a></td>
  </tr>
</table>
<footer>
  <a href="https://rbidocs.rbi.org.in/rdocs/content/pdfs/Accessibility20012026.pdf">Accessibility</a>
  <a href="https://rbidocs.rbi.org.in/rdocs/content/pdfs/Utkarsh202910042026.pdf">Utkarsh</a>
</footer>
</body></html>
"""

MASTER_CIRCULAR_HTML = """
<html><body>
<table class="tablebg">
  <tr><td class="tableheader"><b>Financial Inclusion and Development</b></td></tr>
  <tr><td class="tableheader"><b>Oct 01, 2026</b></td></tr>
  <tr>
    <td><a class='link2' href=BS_ViewMasCirculardetails.aspx?id=13716>Master Circular - Credit Facilities</a></td>
    <td><a href="http://rbidocs.rbi.org.in/rdocs/notification/PDFs/272MC011020266691348260DF4CF99ACE017F146409F1.PDF">PDF</a></td>
  </tr>
</table>
</body></html>
"""

CIRCULAR_INDEX_HTML = """
<html><body>
<table class="tablebg">
  <tr><th>Circular Number</th><th>Date Of Issue</th><th>Department</th><th>Subject</th><th>Meant For</th></tr>
  <tr>
    <td><a class="link2" href="BS_CircularIndexDisplay.aspx?Id=13749">RBI/2026-2027/303<BR>DoR.AML.REC.255/14.06.001/2026-27</a></td>
    <td>30.10.2026</td>
    <td>Department of Regulation</td>
    <td>Implementation of Section 51A of UAPA, 1967</td>
    <td>Commercial Banks</td>
  </tr>
  <tr>
    <td><a class="link2" href="BS_CircularIndexDisplay.aspx?Id=99999">RBI/2026-2027/399</a></td>
    <td>21.11.2026</td>
    <td>Department of Regulation</td>
    <td>New Circular Subject Example</td>
    <td>Commercial Banks</td>
  </tr>
</table>
</body></html>
"""

CIRCULAR_DETAIL_HTML = """
<html><body>
<table class="tablebg">
  <tr><td class="tableheader">
    <a href="https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/NEWCIRC99999.PDF">PDF</a>
  </td></tr>
</table>
<a href="https://rbidocs.rbi.org.in/rdocs/content/pdfs/Accessibility20012026.pdf">Accessibility</a>
</body></html>
"""


class TestSyncPipeline(unittest.TestCase):
    def test_press_release_table_excludes_footer_and_extracts_meta(self):
        fake_resp = mock.Mock(status_code=200, text=PRESS_RELEASE_HTML, headers={})
        with mock.patch.object(rbi_crawler, "_http_get", return_value=fake_resp):
            records, tel = rbi_crawler.crawl_index_records(
                "Press-Releases",
                rbi_crawler.RBI_INDEX_ENDPOINTS["Press-Releases"],
            )
        self.assertEqual(tel["status"], "OK")
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["category"], "Press-Releases")
        self.assertEqual(rec["document_id"], "64017")
        self.assertEqual(rec["listing_date"], "Nov 20, 2026")
        self.assertEqual(rec["iso_date"], "2026-11-20")
        self.assertEqual(rec["headline"], "Conversion/Switch of State Government Securities")
        self.assertTrue(rec["pdf_url"].endswith("PR153980EC0AE092E14AE6963872D7C9520E39.PDF"))

    def test_http_scheme_deduplication(self):
        known_norm = {
            rbi_crawler.normalize_url(
                "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/272MC011020266691348260DF4CF99ACE017F146409F1.PDF"
            )
        }
        fake_resp = mock.Mock(status_code=200, text=MASTER_CIRCULAR_HTML, headers={})
        with mock.patch.object(rbi_crawler, "_http_get", return_value=fake_resp):
            records, tel = rbi_crawler.crawl_index_records(
                "Master-Circulars",
                rbi_crawler.RBI_INDEX_ENDPOINTS["Master-Circulars"],
                known_norm=known_norm,
            )
        self.assertEqual(tel["total_found"], 1)
        self.assertEqual(tel["new_count"], 0)
        self.assertEqual(records, [])

    def test_circular_index_follows_only_unknown_detail_pages(self):
        def fake_get(url, timeout=60, retries=4):
            if "Id=99999" in url:
                return mock.Mock(status_code=200, text=CIRCULAR_DETAIL_HTML, headers={})
            return mock.Mock(status_code=200, text=CIRCULAR_INDEX_HTML, headers={})

        known_keys = {"bs_circularindexdisplay.aspx:id=13749"}
        with mock.patch.object(rbi_crawler, "_http_get", side_effect=fake_get):
            records, tel = rbi_crawler.crawl_index_records(
                "Circular-Index",
                rbi_crawler.RBI_INDEX_ENDPOINTS["Circular-Index"],
                known_listing_keys=known_keys,
            )
        self.assertEqual(tel["detail_fetches"], 1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["category"], "Circulars")
        self.assertEqual(records[0]["listing_date"], "Nov 21, 2026")
        self.assertEqual(records[0]["headline"], "New Circular Subject Example")

    def test_canonical_name_uses_singular_prefix(self):
        info = rbi_crawler.derive_canonical_name(
            "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR153980EC0AE092E14AE6963872D7C9520E39.PDF",
            listing_url="https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=64017",
            headline="Conversion/Switch of State Government Securities",
            listing_date="Nov 20, 2026",
            category="Press-Releases",
            document_id="64017",
        )
        self.assertEqual(info["category"], "Press-Releases")
        self.assertEqual(
            info["file_name"],
            "2026-11-20_Press-Release_64017_Conversion-Switch of State Government Securities.pdf",
        )

    def test_gate_c_verifies_gpg_under_empty_gnupghome(self):
        with tempfile.TemporaryDirectory() as empty_gnupg:
            old = os.environ.get("GNUPGHOME")
            os.environ["GNUPGHOME"] = empty_gnupg
            try:
                passed, total, failures = audit_parity.check_c()
            finally:
                if old is None:
                    os.environ.pop("GNUPGHOME", None)
                else:
                    os.environ["GNUPGHOME"] = old
        self.assertEqual(passed, 1, failures)
        self.assertEqual(total, 1)
        self.assertEqual(failures, [])

    def test_generate_sync_commit_message_includes_all_endpoints_and_telemetry(self):
        with tempfile.TemporaryDirectory() as tmp:
            crawl_p = os.path.join(tmp, "crawl.json")
            reg_p = os.path.join(tmp, "reg.json")
            conv_p = os.path.join(tmp, "conv.json")
            hf_p = os.path.join(tmp, "hf.json")
            with open(crawl_p, "w", encoding="utf-8") as f:
                json.dump({
                    "endpoints": [
                        {"name": k, "url": v, "status": "OK", "http_status": 200, "total_found": 5, "new_count": 1 if k == "Press-Releases" else 0}
                        for k, v in rbi_crawler.RBI_INDEX_ENDPOINTS.items()
                    ],
                    "total_new": 1,
                }, f)
            with open(reg_p, "w", encoding="utf-8") as f:
                json.dump({"discovered_count": 1, "fresh_count": 1, "registered_count": 1, "skipped_count": 0, "hf_uploaded_count": 1}, f)
            with open(conv_p, "w", encoding="utf-8") as f:
                json.dump({
                    "converted_count": 1,
                    "total_pages": 3,
                    "native_pages": 2,
                    "ocr_pages": 1,
                    "engines_used": {"firecrawl-anydoc 0.2.4 + RapidOCR (PP-OCRv5 ONNX)": 1},
                    "verification_statuses": {"VERIFIED_LEVEL_5": 1},
                    "by_category": {"Press-Releases": 1},
                    "documents": [{
                        "doc_id": "64017",
                        "title": "Test Release",
                        "category": "Press-Releases",
                        "year": 2026,
                        "md_path": "data/Press-Releases/2026/test.md",
                        "pdf_url": "https://rbidocs.rbi.org.in/rdocs/test.pdf",
                        "hf_url": "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/test.pdf",
                        "listing_url": "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=64017",
                        "total_pages": 3,
                        "native_pages": 2,
                        "ocr_pages": 1,
                        "engine": "firecrawl-anydoc 0.2.4 + RapidOCR (PP-OCRv5 ONNX)",
                        "verification_status": "VERIFIED_LEVEL_5",
                        "status": "DONE",
                    }],
                }, f)
            with open(hf_p, "w", encoding="utf-8") as f:
                json.dump({"status": "OK", "remote_pdf_count": 88236, "new_count": 0}, f)

            msg = generate_sync_commit_message.build_commit_message(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                mode="sync",
                crawl_report_path=crawl_p,
                register_report_path=reg_p,
                conversion_report_path=conv_p,
                hf_report_path=hf_p,
            )
        for ep_url in rbi_crawler.RBI_INDEX_ENDPOINTS.values():
            self.assertIn(ep_url, msg)
        self.assertIn("https://rbi-archive.pages.dev/mcp", msg)
        self.assertIn("RapidOCR (PP-OCRv5 ONNX)", msg)
        self.assertIn("0 native + 1 OCR", msg.splitlines()[0])
        self.assertIn("12/12", msg)

    def test_register_fail_on_all_skipped_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            new_docs = os.path.join(tmp, "new.json")
            inv = os.path.join(tmp, "inv.jsonl")
            led = os.path.join(tmp, "led.csv")
            urls = os.path.join(tmp, "urls.txt")
            out = os.path.join(tmp, "reg.json")
            rep = os.path.join(tmp, "rep.json")
            with open(new_docs, "w", encoding="utf-8") as f:
                json.dump([{"pdf_url": "https://rbidocs.rbi.org.in/rdocs/bad.pdf"}], f)
            for p in (inv, led, urls):
                open(p, "w", encoding="utf-8").close()
            with mock.patch.object(rbi_crawler, "download_new_pdf", side_effect=rbi_crawler.CrawlError("fail")):
                rc = register_new_documents.main([
                    "--new-documents", new_docs,
                    "--inventory", inv,
                    "--ledger", led,
                    "--urls-file", urls,
                    "--out", out,
                    "--work-dir", tmp,
                    "--pdf-cache-dir", os.path.join(tmp, "pdfs"),
                    "--report-out", rep,
                    "--fail-on-all-skipped",
                ])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
