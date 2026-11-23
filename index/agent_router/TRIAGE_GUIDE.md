# RBI Regulatory Archive: AI Agent Triage and Statutory Hierarchy Guide

Welcome, Agent. This repository contains the complete, authoritative, and lossless archive of all Reserve Bank of India (RBI) regulations from 1991 through 2026 (88,297+ documents) converted to GitHub-Flavored Markdown.

This guide provides a deterministic, zero-hallucination routing protocol for AI agents, RAG engines, and automated legal verification pipelines to locate controlling RBI regulations in $\le 3$ tool calls.

---

## 1. Statutory Regulatory Hierarchy (5 Tiers)

The Reserve Bank of India governs the Indian financial ecosystem under a strict statutory hierarchy. When answering legal, compliance, or regulatory queries, agents must prioritize controlling law over operational circulars:

### Tier 1: Controlling Law & Consolidated Master Directions (Highest Authority)
- **Primary Source:** `data/Master-Directions/`
- **Statutory Authority:**
  - Section 35A & Section 21, Banking Regulation Act, 1949
  - Section 45JA, 45L, 45M, & 45W, Reserve Bank of India Act, 1934
  - Sections 10(4), 11(1), & 11(2), Foreign Exchange Management Act (FEMA), 1999
  - Section 10(2) & Section 18, Payment and Settlement Systems Act, 2007
  - Sections 29A & 30A, National Housing Bank Act, 1987 / RBI Act (for HFCs)
- **Operational Rule for Agents:** Master Directions consolidate all previous circulars and notifications on a regulatory subject. They are updated dynamically by the RBI. Whenever an agent needs the prevailing rule or current standard on any topic (e.g. KYC, Capital Adequacy, Basel III, Priority Sector Lending, Digital Lending, Outsourcing), the agent **MUST** cite the corresponding Master Direction first.
- **Index:** `index/agent_router/active_master_directions_by_entity.md` and `.json`.

### Tier 2: Operational Directives & In-Year Circulars
- **Primary Sources:** `data/Notifications/` and `data/Circulars/`
- **Role:** Specific operational instructions, immediate policy rate revisions (Repo/Reverse Repo/SDF), regulatory reporting formats, or interim amendments issued between annual consolidations of Master Directions.
- **Operational Rule for Agents:** If an inquiry asks about a specific circular number (e.g., `RBI/2025-26/123`), look it up directly via `index/agent_router/circular_ref_to_path.json`. To verify whether a circular amends or is superseded by a Master Direction, check `index/agent_router/citation_and_consequence_graph.jsonl`.

### Tier 3: Draft Guidelines & Consultative Documents
- **Primary Source:** `data/Draft-Notifications-Guidelines/`
- **Role:** Proposed regulatory frameworks released for public comments and stakeholder feedback (e.g. Draft Framework on Climate Risk, Draft Directions on Project Finance).
- **Operational Rule for Agents:** **NON-BINDING.** Agents must never present draft guidelines as enforceable law. Always qualify citations with *"Draft / For feedback only."*

### Tier 4: Penal Consequences & Enforcement Actions
- **Primary Source:** `data/Press-Releases/` (Enforcement subset)
- **Statutory Authority:**
  - Section 47A(1)(c) read with Section 46(4)(i), Banking Regulation Act, 1949
  - Section 58G(1)(a) read with Section 58B(5)(aa), Reserve Bank of India Act, 1934
- **Role:** Monetary penalties, directions on operations (e.g. restriction on onboarding new customers), license cancellations, or compounding of FEMA violations.
- **Operational Rule for Agents:** Look up penal precedents in `index/agent_router/citation_and_consequence_graph.jsonl` under the relationship `PENALIZES_UNDER`.

### Tier 5: Routine Market Operations & Administrative Notices
- **Primary Source:** `data/Press-Releases/` (Market Operations)
- **Role:** Daily Money Market Operations, Sovereign Gold Bond issuances, Treasury Bill auction results, holiday calendars, press conferences.
- **Operational Rule for Agents:** Ephemeral operational announcements. Do not cite as substantive statutory doctrine.

---

## 2. Deterministic Agent Retrieval Protocol (<= 3 Tool Calls)

Follow these exact routes to retrieve regulations deterministically:

### Route A: Lookup by Regulated Entity & Topic (Controlling Law)
1. **Tool Call 1:** Read `index/agent_router/active_master_directions_by_entity.json` or `.md`.
2. **Tool Call 2:** Locate the section for your entity (`Commercial Banks`, `NBFCs`, `UCBs`, `Payment Systems`, `FEMA`, etc.) and find the matching subject.
3. **Tool Call 3:** Read the target `data/Master-Directions/<Year>/<file>.md`.

### Route B: Lookup by RBI Circular Reference (e.g. RBI/2024-25/102 or DOR.No...)
1. **Tool Call 1:** Read `index/agent_router/circular_ref_to_path.json` (or lookup target key).
2. **Tool Call 2:** Retrieve the relative path `data/<Folder>/<Year>/<file>.md`.
3. **Tool Call 3:** Read the document or check `index/agent_router/citation_and_consequence_graph.jsonl` for amendments/supersession.

### Route C: Lookup by URL (Direct RBI URL or Hugging Face URL)
1. **Tool Call 1:** Compute `shard = sha256(url.strip().lower())[:2]` (e.g. `a3`).
2. **Tool Call 2:** Read `index/url_shards/<shard>.json` and get `data/<path>.md`.
3. **Tool Call 3:** Read `data/<path>.md`.

---

## 3. Directory Structure Summary

```
rbi-regulatory-archive-1991-2026/
├── INDEX.md                                   # Root Master Index
├── llms.txt / llms-full.txt                   # LLM Entry Points
├── STATE.json                                 # High-level conversion census (<500 bytes)
├── index/
│   ├── agent_router/
│   │   ├── TRIAGE_GUIDE.md                    # This guide
│   │   ├── AEO_REGULATORY_FAQ.md              # Statutory answer engine Q&A
│   │   ├── active_master_directions_by_entity.md # MDs grouped by regulated entity
│   │   ├── active_master_directions_by_entity.json # Machine-readable MDs by entity
│   │   ├── circular_ref_to_path.json          # Circular ref -> file path
│   │   └── citation_and_consequence_graph.jsonl # Causal citations & consequences
│   ├── by_category/                           # Category-level indexes (6 folders)
│   ├── by_year/                               # Yearly indexes (1991-2026)
│   └── url_shards/                            # 256 compact URL shards (00.json..ff.json)
├── data/
│   ├── Master-Directions/<YYYY>/INDEX.md      # Per-directory index
│   ├── Notifications/<YYYY>/INDEX.md
│   ├── Master-Circulars/<YYYY>/INDEX.md
│   ├── Draft-Notifications-Guidelines/<YYYY>/INDEX.md
│   ├── Circulars/<YYYY>/INDEX.md
│   └── Press-Releases/<YYYY>/INDEX.md
└── manifest/
    ├── catalog/<YYYY>.jsonl                   # Yearly sharded JSONL catalog
    ├── sha256_conversion_ledger.csv           # Source of truth ledger
    └── pdf_final_direct_urls.txt              # Direct RBI endpoint catalog
```
