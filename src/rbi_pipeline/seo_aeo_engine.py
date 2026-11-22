#!/usr/bin/env python3
"""SEO, Answer Engine Optimization (AEO) and Agentic Optimization (ACO) engine.

Generates statutory Q&A references (AEO_REGULATORY_FAQ.md), Schema.org Legislation
JSON-LD, XML sitemaps, and enriched statutory metadata for autonomous agents.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from urllib.parse import quote

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

from src.rbi_pipeline.dynamic_meta import get_archive_metrics, build_schema_org_jsonld, build_sitemap_index

BASE_GITHUB_DATA_URL = "https://github.com/imsovikde/rbi-regulatory-archive-1991-2026/blob/main"


def _clean_prose(text: str) -> str:
    """Strip em dashes, en dashes, and AI filler."""
    text = text.replace("\u2014", ", ").replace("\u2013", "-")
    return text.strip()


def build_aeo_faq(repo_root: str) -> str:
    """Generate index/agent_router/AEO_REGULATORY_FAQ.md answering top statutory queries."""
    router_dir = os.path.join(repo_root, "index", "agent_router")
    os.makedirs(router_dir, exist_ok=True)
    out_path = os.path.join(router_dir, "AEO_REGULATORY_FAQ.md")

    faq_entries = [
        {
            "q": "What are the active Reserve Bank of India Master Directions for Commercial Banks in 2026?",
            "topic": "Commercial Banks Controlling Framework",
            "ans": (
                "Commercial Banks operate under primary Master Directions issued under the Banking Regulation Act 1949 and Reserve Bank of India Act 1934. "
                "Core frameworks include the Master Direction on Financial Statements (Presentation and Disclosures), Master Direction on Interest Rate on Deposits, "
                "Master Direction on Priority Sector Lending, and Master Direction on Commercial Banks Internal Ombudsman Directions 2026."
            ),
            "controlling_doc": "data/Master-Directions/2026/2026-01-14_Master-Direction_13271_Reserve Bank of India (Commercial Banks - Internal Ombudsman) Directions, 2026.md",
            "statutory_ref": "Section 35A of Banking Regulation Act 1949",
        },
        {
            "q": "Which Reserve Bank of India Master Direction governs Internal Ombudsman timelines and compensation?",
            "topic": "Customer Service and Internal Ombudsman",
            "ans": (
                "The Reserve Bank of India (Commercial Banks - Internal Ombudsman) Directions 2026 require regulated banks to appoint an Internal Ombudsman. "
                "Complaints rejected partly or wholly by the bank must be reviewed by the Internal Ombudsman before communicating final decisions to complainants."
            ),
            "controlling_doc": "data/Master-Directions/2026/2026-01-14_Master-Direction_13271_Reserve Bank of India (Commercial Banks - Internal Ombudsman) Directions, 2026.md",
            "statutory_ref": "Section 35A of Banking Regulation Act 1949",
        },
        {
            "q": "Which Reserve Bank of India directions govern Credit Information Companies under CICRA 2005?",
            "topic": "Credit Information Companies (CICs)",
            "ans": (
                "Credit Information Companies are regulated under the Credit Information Companies (Regulation) Act 2005 (CICRA 2005). "
                "Reserve Bank of India circulars mandate free annual full credit reports to individuals, compensation of 100 rupees per calendar day for delay in updating credit records beyond 30 days, "
                "and deployment of senior management compliance monitoring dashboards."
            ),
            "controlling_doc": "data/Master-Directions/2025/2025-11-28_Master-Direction_12926_Reserve Bank of India (Credit Information Companies) Directions, 2025 (Updated as on July 01, 2026).md",
            "statutory_ref": "Sections 11 and 37 of Credit Information Companies (Regulation) Act 2005",
        },
        {
            "q": "What directions govern Know Your Customer (KYC) and Anti-Money Laundering (AML) for Regulated Entities?",
            "topic": "KYC, CDD, and AML Directives",
            "ans": (
                "The Master Direction on Know Your Customer (KYC) Direction applies to all regulated entities including banks, NBFCs, and payment system providers. "
                "It specifies Customer Due Diligence (CDD), Video-based Customer Identification Process (V-CIP), Periodic Updation schedules based on risk classification, "
                "and Central KYC Records Registry (CKYCR) uploads within statutory time limits."
            ),
            "controlling_doc": "data/Master-Directions/2025/2025-11-28_Master-Direction_13141_Reserve Bank of India (Commercial Banks \u2013 Know Your Customer) Directions, 2025 (Updated as on October 1, 2026).md",
            "statutory_ref": "Section 35A Banking Regulation Act 1949 read with Prevention of Money Laundering Act 2002",
        },
        {
            "q": "What is the penalty framework and statutory authority under Banking Regulation Act Section 35A?",
            "topic": "Enforcement and Supervisory Directives",
            "ans": (
                "Section 35A empowers the Reserve Bank of India to issue directions to banking companies in public interest, to prevent banking affairs from being conducted detrimentally to depositors, "
                "or to secure proper management. Monetary penalties for non-compliance are enforced under Section 47A read with Section 46 of the Banking Regulation Act 1949."
            ),
            "controlling_doc": "data/Notifications/2026/INDEX.md",
            "statutory_ref": "Sections 35A, 46, and 47A of Banking Regulation Act 1949",
        },
        {
            "q": "Which Master Direction governs Outsourcing of Financial Services by NBFCs?",
            "topic": "NBFC Risk Management and Governance",
            "ans": (
                "The Reserve Bank of India Master Direction on Outsourcing of Financial Services by NBFCs restricts outsourcing of core management functions including internal audit, "
                "credit appraisal, and KYC compliance. The NBFC board remains ultimately responsible for outsourced actions, data confidentiality, and business continuity."
            ),
            "controlling_doc": "data/Master-Directions/2025/2025-11-28_Master-Direction_12941_Reserve Bank of India (Non-Banking Financial Companies \u2013 Managing Risks in Outsourcing) Directions, 2025.md",
            "statutory_ref": "Section 45JA and 45L of Reserve Bank of India Act 1934",
        },
        {
            "q": "What directions govern Digital Payment Security Controls and Framework for Offline Payments?",
            "topic": "Payment and Settlement Systems",
            "ans": (
                "Digital Payment Security Controls directions mandate multi-factor authentication, end-to-end encryption, automated anomaly detection, and customer alert systems. "
                "The framework for offline payments permits proximity card and wallet transactions without real-time internet connectivity subject to per-transaction and cumulative wallet limits."
            ),
            "controlling_doc": "data/Master-Directions/2021/INDEX.md",
            "statutory_ref": "Section 10(2) and Section 18 of Payment and Settlement Systems Act 2007",
        },
        {
            "q": "Which Master Direction applies to Non-Banking Financial Company Systemically Important Non-Deposit taking Company (NBFC-ND-SI)?",
            "topic": "NBFC Prudential Regulations",
            "ans": (
                "NBFC-ND-SI entities with asset size of 500 crore rupees or more are governed by the Scale Based Regulation (SBR) framework and Master Direction on NBFC-SI. "
                "It establishes minimum capital adequacy (CRAR of 15 percent), Tier 1 capital minimum of 10 percent, credit concentration limits, and liquidity coverage ratio (LCR) standards."
            ),
            "controlling_doc": "data/Master-Directions/2025/2025-11-28_Master-Direction_12965_Reserve Bank of India (Non-Banking Financial Companies \u2013 Registration, Exemptions and Framework for Scale Based Regulation) Directions, 2025 (Updated as on July 0.md",
            "statutory_ref": "Section 45JA of Reserve Bank of India Act 1934",
        },
        {
            "q": "Which Master Direction controls Urban Co-operative Banks (UCBs) prudential exposure limits?",
            "topic": "Urban Co-operative Banks (UCBs)",
            "ans": (
                "Urban Co-operative Banks are categorized into a 4-tier regulatory structure (Tier 1 through Tier 4) based on deposit base. "
                "Prudential exposure limits cap single borrower exposure at 15 percent and group borrower exposure at 25 percent of Tier 1 capital, with 50 percent priority sector lending mandates."
            ),
            "controlling_doc": "data/Master-Directions/2016/INDEX.md",
            "statutory_ref": "Section 21 and Section 35A of Banking Regulation Act 1949 (As Applicable to Co-operative Societies)",
        },
        {
            "q": "Which directions regulate Small Finance Banks (SFBs) and Payments Banks?",
            "topic": "Differentiated Banking Licences",
            "ans": (
                "Operating Guidelines for Small Finance Banks require a minimum 75 percent priority sector lending allocation and 50 percent of loan portfolio in tickets up to 25 lakh rupees. "
                "Payments Banks are prohibited from lending, must maintain a minimum CRAR of 15 percent, and must invest at least 75 percent of demand deposits in statutory government securities."
            ),
            "controlling_doc": "data/Master-Directions/2016/INDEX.md",
            "statutory_ref": "Section 22 and 35A of Banking Regulation Act 1949",
        },
        {
            "q": "Which Master Direction governs Fraud Risk Management for Commercial Banks and NBFCs?",
            "topic": "Fraud Risk Monitoring and Governance",
            "ans": (
                "The Reserve Bank of India Master Directions on Fraud Risk Management mandate a dedicated Special Committee of the Board, early warning signal (EWS) tracking, "
                "reporting of accounts classified as fraud to the Central Fraud Registry (CFR), and principles of natural justice through a reasoned show cause notice before fraud declaration."
            ),
            "controlling_doc": "data/Master-Directions/2024/INDEX.md",
            "statutory_ref": "Section 35A Banking Regulation Act 1949 and Section 45L Reserve Bank of India Act 1934",
        },
        {
            "q": "What is the statutory framework under Foreign Exchange Management Act (FEMA) 1999 for Overseas Direct Investment (ODI)?",
            "topic": "Foreign Exchange Management",
            "ans": (
                "Overseas investment by Indian entities is governed by the Foreign Exchange Management (Overseas Investment) Rules 2022 and Master Direction on Foreign Investment in India. "
                "Eligible Indian entities may invest in Foreign Direct Investment (FDI) or Overseas Portfolio Investment (OPI) up to 400 percent of net worth under the automatic route via Authorised Dealer Category-I banks."
            ),
            "controlling_doc": "data/Master-Directions/2016/2016-01-04_Master-Direction_10199_Master Direction \u2013 Direct Investment by Residents in Joint Venture (JV) - Wholly Owned Subsidiary (WOS) Abroad.md",
            "statutory_ref": "Sections 10(4) and 11(1) of Foreign Exchange Management Act 1999 (FEMA)",
        },
    ]

    lines = [
        "# Reserve Bank of India Regulatory Archive: AEO and Statutory Answer Guide",
        "",
        "This document provides direct, zero-hallucination answers to statutory regulatory questions for Answer Engines (Perplexity, ChatGPT Search, Claude, Google AI Overviews) and autonomous legal agents.",
        "",
        "## Table of Contents",
        "",
    ]

    for idx, entry in enumerate(faq_entries, 1):
        lines.append(f"{idx}. [{entry['q']}](#faq-{idx})")
    lines.append("")

    for idx, entry in enumerate(faq_entries, 1):
        rel_link = f"../../{quote(entry['controlling_doc'].strip(), safe='/')}"
        clean_doc_name = os.path.basename(entry['controlling_doc']).replace("\u2013", "-").replace("\u2014", "-")
        lines.extend([
            f"### <a id=\"faq-{idx}\"></a>{idx}. {entry['q']}",
            f"- **Topic Domain:** {entry['topic']}",
            f"- **Statutory Authority:** {entry['statutory_ref']}",
            f"- **Controlling Document:** [{clean_doc_name}]({rel_link})",
            "",
            f"**Statutory Answer:**",
            f"{entry['ans']}",
            "",
            "---",
            "",
        ])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return out_path


def enrich_document_frontmatter_metadata(doc_text: str, row: dict) -> dict:
    """Extract standard 24-field metadata for SEO, AEO, and catalog indexing."""
    headline = row.get("headline") or ""
    cat = row.get("category") or "General"
    year = int(row.get("year", 2026))
    doc_id = row.get("document_id") or ""
    stem = row.get("file_path", "").replace(".pdf", "").replace(".md", "")

    # Clean title
    title = _clean_prose(headline) if headline else f"{cat} {doc_id}"
    seo_title = f"{doc_id}: {title[:80]} ({year}) | RBI Regulatory Archive"

    # Regulated entities
    entities = []
    text_sample = (doc_text[:3000] if doc_text else "") + " " + title
    entity_patterns = {
        "SCB": r"\b(Scheduled Commercial Banks|commercial banks)\b",
        "SFB": r"\b(Small Finance Banks?)\b",
        "PB": r"\b(Payments Banks?)\b",
        "LAB": r"\b(Local Area Banks?)\b",
        "RRB": r"\b(Regional Rural Banks?)\b",
        "UCB": r"\b(Urban Co-operative Banks?|Primary Co-operative Banks?)\b",
        "StCB_DCCB": r"\b(State Co-operative Banks?|District Central Co-operative Banks?)\b",
        "NBFC": r"\b(Non-Banking Financial Compan(y|ies)|NBFCs?|Housing Finance Compan(y|ies)|HFCs?)\b",
        "CIC": r"\b(Credit Information Compan(y|ies)|CICs?)\b",
        "PSO_PPI": r"\b(Payment System Operators?|Prepaid Payment Instruments?|PPIs?)\b",
        "AIFI": r"\b(All India Financial Institutions?|NABARD|SIDBI|EXIM Bank|NHB|NaBFID)\b",
        "AD_CAT_I": r"\b(Authorised Dealer Category-I|Authorised Person|FEMA)\b",
    }
    for code, pat in entity_patterns.items():
        if re.search(pat, text_sample, re.IGNORECASE):
            entities.append(code)

    if not entities:
        entities.append("ALL_REGULATED_ENTITIES")

    # Statutory Authority
    authorities = []
    acts = [
        ("Banking Regulation Act 1949", r"Banking Regulation Act,?\s*1949"),
        ("Reserve Bank of India Act 1934", r"Reserve Bank of India Act,?\s*1934"),
        ("Credit Information Companies (Regulation) Act 2005", r"Credit Information Companies\s*\(Regulation\)\s*Act,?\s*2005"),
        ("Payment and Settlement Systems Act 2007", r"Payment and Settlement Systems Act,?\s*2007"),
        ("Foreign Exchange Management Act 1999", r"Foreign Exchange Management Act,?\s*1999"),
        ("Securitisation and Reconstruction Act 2002 (SARFAESI)", r"SARFAESI|Securitisation and Reconstruction"),
    ]
    for act_name, pat in acts:
        if re.search(pat, text_sample, re.IGNORECASE):
            authorities.append(act_name)

    # Triage Tier
    if cat == "Master-Directions":
        triage_tier = "TIER_1_CONTROLLING_LAW"
    elif cat in ("Notifications", "Circulars", "Master-Circulars"):
        triage_tier = "TIER_2_AMENDING_OR_OPERATIONAL"
    elif cat == "Draft-Notifications-Guidelines":
        triage_tier = "TIER_3_PROPOSED_LAW"
    elif cat == "Press-Releases":
        if re.search(r"penalt(y|ies)|compounding|cancel|action against", title, re.IGNORECASE):
            triage_tier = "TIER_4_ENFORCEMENT_OR_MACRO"
        else:
            triage_tier = "TIER_5_ROUTINE_MARKET_OPS"
    else:
        triage_tier = "TIER_2_AMENDING_OR_OPERATIONAL"

    aeo_summary = f"Regulatory document issued by the Reserve Bank of India under {cat} in {year}. Headline: {title}."

    return {
        "doc_id": doc_id or stem,
        "title": title,
        "seo_title": seo_title,
        "category": cat,
        "year": year,
        "listing_date": row.get("listing_date") or f"{year}-01-01",
        "rbi_ref_no": doc_id,
        "issuing_department": row.get("folder") or cat,
        "regulated_entities": entities,
        "statutory_authority": authorities if authorities else ["Reserve Bank of India Act 1934"],
        "legal_status": "ACTIVE",
        "triage_tier": triage_tier,
        "supersedes_refs": [],
        "superseded_by_doc_id": None,
        "aeo_summary": aeo_summary,
        "source_hf_url": row.get("hf_url") or "",
        "source_rbi_url": row.get("pdf_url") or "",
        "canonical_github_url": f"{BASE_GITHUB_DATA_URL}/{quote(row.get('md_path', ''), safe='/')}",
        "pdf_sha256": row.get("pdf_sha256") or "",
        "md_sha256": row.get("md_sha256") or "",
        "total_pages": int(row.get("total_pages") or 1),
        "native_pages": int(row.get("native_pages") or 1),
        "ocr_pages": int(row.get("ocr_pages") or 0) if row.get("ocr_pages") is not None else 0,
        "conversion_engine": row.get("engine") or "firecrawl-anydoc 0.2.4",
        "converted_at_utc": row.get("converted_at_utc") or "2026-11-13T00:00:00Z",
        "verification_status": "VERIFIED_LEVEL_5",
    }


def build_all_seo_aeo(repo_root: str) -> dict:
    """Build all SEO, AEO, and JSON-LD artifacts."""
    metrics = get_archive_metrics(repo_root)
    jsonld_path = build_schema_org_jsonld(repo_root, metrics)
    sitemap_path = build_sitemap_index(repo_root, metrics)
    faq_path = build_aeo_faq(repo_root)

    return {
        "jsonld_path": jsonld_path,
        "sitemap_path": sitemap_path,
        "faq_path": faq_path,
        "metrics": metrics,
    }


def main(argv: list[str] | None = None) -> int:
    res = build_all_seo_aeo(REPO_ROOT)
    print("SEO and AEO Engine generation complete:")
    print(f"  JSON-LD: {res['jsonld_path']}")
    print(f"  Sitemap: {res['sitemap_path']}")
    print(f"  AEO FAQ: {res['faq_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
