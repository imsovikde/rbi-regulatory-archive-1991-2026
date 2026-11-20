# RBI Regulatory Archive (1991-2026): Model Context Protocol (MCP), Local CLI & Web Portal Guide

[![Public Web Portal](https://img.shields.io/badge/Web_Portal-https%3A%2F%2Frbi--archive.pages.dev-blue.svg)](https://rbi-archive.pages.dev)
[![Official MCP Endpoint](https://img.shields.io/badge/MCP_Endpoint-https%3A%2F%2Frbi--archive.pages.dev%2Fmcp-green.svg)](https://rbi-archive.pages.dev/mcp)
[![npm CLI Package](https://img.shields.io/npm/v/rbi-doc-mcp.svg?label=npx%20rbi-doc-mcp%20--local)](https://www.npmjs.com/package/rbi-doc-mcp)

This guide explains how to connect AI assistants, code editors, compliance workflows, and local terminals to the **Reserve Bank of India (RBI) Regulatory Archive (1991-2026, 88,236 documents)** over the **Model Context Protocol (MCP)** or via the offline-capable **`npx rbi-doc-mcp --local`** CLI.

---

## 1. Official Public Endpoints & Package Registry

| Surface | Canonical URL / Command | Purpose |
| :--- | :--- | :--- |
| Public Web Portal & Interactive Terminal | `https://rbi-archive.pages.dev` | Browser-based BM25F regulatory search, statutory graph explorer, point-in-time validity verifier, and judicial citation formatter |
| Official Streamable HTTP MCP Endpoint | `https://rbi-archive.pages.dev/mcp` | Remote MCP 2025-06-18 Streamable HTTP and JSON-RPC 2.0 endpoint for Claude, Cursor, VS Code, Windsurf, and custom agents |
| Local Stdio MCP Server & CLI (`npm`) | `npx rbi-doc-mcp --local` | Offline-capable local `stdio` MCP server and CLI backed by static BM25F shards and GitHub Raw / Hugging Face document mirrors |
| User Account & Usage Dashboard | `https://rbi-archive.pages.dev/account` | Personal usage metrics (24h / 7d / 30d), per-tool breakdown, active OAuth session list, and one-click session revocation |
| Sign In / Create Free Account | `https://rbi-archive.pages.dev/auth/signin` | Direct browser sign-in, free account registration (`120 req/min`), and instant anonymous session activation (`30 req/min`) |
| OAuth 2.1 Protected Resource Metadata | `https://rbi-archive.pages.dev/.well-known/oauth-protected-resource` | RFC 9728 protected resource discovery for MCP clients |
| OAuth 2.1 Authorization Server Metadata | `https://rbi-archive.pages.dev/.well-known/oauth-authorization-server` | RFC 8414 OAuth 2.1 + PKCE (`S256`) and Dynamic Client Registration discovery |

---

## 2. Two Ways to Connect: Remote Streamable HTTP vs. Local CLI (`npx rbi-doc-mcp --local`)

You can query the 88,236-document archive in two ways:

1. **Remote Streamable HTTP (`https://rbi-archive.pages.dev/mcp`)**:
   - Zero local disk footprint.
   - Exposes all 8 public MCP tools, including clause-level RAG (`rag_query_rbi_provisions`) and multi-hop sandboxed JavaScript execution (`rbi_doc_execute_code`).
   - Supports browser-based OAuth 2.1 + PKCE (`S256`) with **Sign In**, **Create Account**, or **Continue Anonymously**, plus live usage tracking at `https://rbi-archive.pages.dev/account`.
2. **Local Stdio CLI (`npx rbi-doc-mcp --local`)**:
   - Runs locally on Node.js (`>= 18`) over `stdio` with **zero remote API rate limits**.
   - Downloads and caches compact static BM25F, metadata, alias, and validity DAG shards from `https://rbi-archive.pages.dev/idx/v2` into `~/.cache/rbi-doc-mcp/idx-v2`.
   - Fetches full regulatory Markdown directly from `raw.githubusercontent.com/imsovikde/rbi-regulatory-archive-1991-2026` with automatic fallback to `huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026`.

### Direct Terminal Commands (`npx rbi-doc-mcp`)

Beyond running as an MCP `stdio` server, `npx rbi-doc-mcp` supports direct one-liner queries from any shell:

```bash
# Start the local stdio MCP server for Claude Desktop, Cursor, or VS Code
npx rbi-doc-mcp --local

# Run an instant BM25F regulatory search from your terminal
npx rbi-doc-mcp --search "Know Your Customer Master Direction"

# Resolve an official RBI circular reference number or canonical doc_id
npx rbi-doc-mcp --resolve "RBI/2017-18/15"

# Verify whether a circular was legally in force on a specific date
npx rbi-doc-mcp --validity "rbi_081878" 2026-01-01

# Print CLI version and help
npx rbi-doc-mcp --version
npx rbi-doc-mcp --help
```

---

## 3. Step-by-Step Client Setup

### Claude Code (CLI)

**Option A: Remote Streamable HTTP (Recommended for full 8-tool access)**

```bash
claude mcp add --transport http rbi-archive https://rbi-archive.pages.dev/mcp
```

**Option B: Local Stdio Mode (`npx rbi-doc-mcp --local`)**

```bash
claude mcp add rbi-archive-local -- npx -y rbi-doc-mcp --local
```

### Claude (Web & Desktop Custom Connectors)

1. Open Claude Settings and go to **Connectors** (or **Integrations**).
2. Click **Add Custom Connector**.
3. Enter the name `RBI Regulatory Archive` and the Server URL:
   ```text
   https://rbi-archive.pages.dev/mcp
   ```
4. When the authorization window opens at `https://rbi-archive.pages.dev/oauth/authorize`, pick your access tier:
   - **Sign In**: Use your registered email and password (`120 req/min` + Code Mode).
   - **Create Account**: Register a free account in one step.
   - **Continue Anonymously**: Authorize an immediate read-only session (`30 req/min`) without creating an account.

For **Claude Desktop** (`%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS), you can configure either the remote endpoint or the local `npx` command:

```json
{
  "mcpServers": {
    "rbi-archive": {
      "url": "https://rbi-archive.pages.dev/mcp"
    },
    "rbi-archive-local": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp", "--local"]
    }
  }
}
```

### Cursor

Create or edit `.cursor/mcp.json` in your workspace (or `~/.cursor/mcp.json` globally):

```json
{
  "mcpServers": {
    "rbi-archive": {
      "url": "https://rbi-archive.pages.dev/mcp"
    },
    "rbi-archive-local": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp", "--local"]
    }
  }
}
```

### VS Code / GitHub Copilot

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "rbi-archive": {
      "type": "http",
      "url": "https://rbi-archive.pages.dev/mcp"
    },
    "rbi-archive-local": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp", "--local"]
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "rbi-archive": {
      "serverUrl": "https://rbi-archive.pages.dev/mcp"
    },
    "rbi-archive-local": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp", "--local"]
    }
  }
}
```

### Generic Streamable HTTP MCP Clients (cURL / Python / TypeScript)

```bash
curl -sS -X POST https://rbi-archive.pages.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "search_rbi_regulations",
      "arguments": {
        "query": "Know Your Customer Master Direction",
        "limit": 3
      }
    }
  }'
```

---

## 4. Account & Access Tiers

All users have access to the complete 1991-2026 regulatory corpus at zero cost.

| Capability | Continue Anonymously (`anonymous`) | Free Registered Account (`registered`) | Local Stdio CLI (`npx rbi-doc-mcp --local`) |
| :--- | :--- | :--- | :--- |
| Cost | Free | Free | Free |
| Registration required | None | Email + password (`10-128` chars) | None |
| Throughput limit | `30` requests / minute | `120` requests / minute | Unlimited local execution |
| Granted OAuth scopes | `rbi:read` | `rbi:read rbi:code_mode` | Local `stdio` read tools |
| Canonical search, resolution, markdown, validity & citation tools | Enabled | Enabled | Enabled |
| Multi-step Code Mode (`rbi_doc_execute_code`) | Requires registered account | Enabled | Remote HTTP only |
| Usage dashboard & session management | Session view at `/account` | Full 7-day chart, top tools, and session revocation at `https://rbi-archive.pages.dev/account` | Local disk cache (`~/.cache/rbi-doc-mcp/idx-v2`) |

---

## 5. Complete Public Tool Reference & Example Prompts

### 5.1 `search_rbi_regulations`

Hybrid BM25F (`k1 = 1.2`, `b = 0.75`) and 128-dim semantic search across all 88,236 RBI Master Directions, Circulars, Notifications, Draft Guidelines, and Press Releases (1991-2026) with validity-prior modulation.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | Yes | Search keywords, circular subject, or statutory concept |
| `limit` | `number` | No | Maximum results to return (default `5`, max `20`) |
| `category` | `string` | No | Filter by `Master-Directions`, `Master-Circulars`, `Circulars`, `Notifications`, `Draft-Notifications-Guidelines`, or `Press-Releases` |
| `year` | `number` | No | Filter by publication year (`1991` to `2026`) |
| `statute` | `string` | No | Filter by governing statute (`BR_ACT_1949`, `RBI_ACT_1934`, `FEMA_1999`, `PMLA_2002`, `PSS_ACT_2007`, `SARFAESI_2002`) |

**Example prompt:**
> "Search RBI Master Directions and Circulars for digital lending default loss guarantee (FLDG) caps and list the controlling circulars with their effective dates."

### 5.2 `fetch_rbi_markdown`

Retrieves the full SHA-256-verified GitHub-Flavored Markdown text of any RBI regulatory document by its canonical `doc_id`, with optional section extraction.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical document ID (for example `rbi_081878` or `MD_106`) |
| `section` | `string` | No | Optional heading or section filter (`Applicability`, `Definitions`, `Penalties`) |

**Example prompt:**
> "Fetch the full markdown text of RBI circular `rbi_081878` on limiting customer liability in unauthorized electronic banking transactions and summarize the Table-1 reporting timeline."

### 5.3 `resolve_rbi_doc`

Resolves any official RBI circular reference number (`RBI/2017-18/15`, `DOR.No...`, `DBOD.No...`, `DNBS(PD).CC.No...`), notification number, RBI URL (`?Id=13143`), or file path into canonical metadata, publication date, SHA-256 digest, and archive paths.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `identifier` | `string` | Yes | Circular reference number, notification number, numeric ID, RBI URL, or title fragment |

**Example prompt:**
> "Resolve RBI circular reference `RBI/2017-18/15` into its canonical document ID, title, SHA-256 checksum, and Markdown path."

### 5.4 `trace_statutory_consequences`

Traces the causal statutory graph (`SUPERSEDES`, `AMENDS`, `REPEALS`, `CITES`) for a document, along with linked statutory penalties (such as Section 47A(1)(c) of the Banking Regulation Act, 1949) and mandatory compliance turnaround times (TATs).

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical document ID to trace across the statutory DAG |

**Example prompt:**
> "Trace the statutory amendment chain, penalty provisions, and compliance turnaround times for RBI document `13143`."

### 5.5 `verify_circular_validity`

Evaluates point-in-time legal validity (`ACTIVE`, `SUPERSEDED`, or `REPEALED`) for any circular on a given `YYYY-MM-DD` date by traversing incoming supersession and repeal edges in the statutory DAG.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical document ID to check |
| `as_of_date` | `string` | No | ISO calendar date (`YYYY-MM-DD`); defaults to today |

**Example prompt:**
> "Verify whether RBI circular `rbi_081878` (`RBI/2017-18/15`) was legally in force on `2020-04-01` and `2026-01-15`."

### 5.6 `format_court_citation`

Generates a formal judicial citation string suitable for Supreme Court of India, High Court, NCLAT, and regulatory compliance filings, complete with the official RBI reference number, date, statutory authority, and SHA-256 verification digest.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `identifier` | `string` | Yes | Canonical `doc_id` or official RBI circular number |

**Example prompt:**
> "Format a court-ready legal citation with SHA-256 verification digest for RBI circular `RBI/2017-18/15`."

### 5.7 `rag_query_rbi_provisions`

Performs clause-level retrieval-augmented generation (RAG) over Content-Defined Chunked (CDC) statutory provisions, returning the highest-scoring passages with exact document citations and section headers.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | Yes | Natural-language compliance question or statutory provision query |
| `top_k` | `number` | No | Number of provision chunks to retrieve (default `5`, max `15`) |
| `category` | `string` | No | Optional category filter |
| `year` | `number` | No | Optional year filter |

**Example prompt:**
> "Retrieve the exact RBI statutory provisions governing Video-based Customer Identification Process (V-CIP) audit trails and concurrent auditor verification under the KYC Master Direction."

### 5.8 `rbi_doc_execute_code`

Executes a single-turn, time-bounded JavaScript query program against the read-only `sdk` interface (`sdk.search`, `sdk.resolve`, `sdk.checkValidity`, `sdk.traceConsequences`, `sdk.cite`, `sdk.ragQuery`) so an agent can join and filter multiple lookups in one round-trip.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `code` | `string` | Yes | Async JavaScript snippet using `sdk.*` methods and returning a JSON-serializable value |

**Example `code` argument:**

```javascript
const hits = await sdk.search({ query: "Know Your Customer", category: "Master-Directions", limit: 3 });
const enriched = [];
for (const doc of hits) {
  const validity = await sdk.checkValidity(doc.doc_id);
  const citation = await sdk.cite(doc.doc_id);
  enriched.push({
    doc_id: doc.doc_id,
    title: doc.title,
    status: validity.status,
    citation: citation.judicial_citation
  });
}
return enriched;
```

---

## 6. Frequently Asked Questions (AEO & Compliance Reference)

### How do I query Reserve Bank of India (RBI) circulars in Claude, Cursor, or VS Code without downloading the entire 88,236-file repository?
Connect your MCP client to `https://rbi-archive.pages.dev/mcp` over Streamable HTTP (`claude mcp add --transport http rbi-archive https://rbi-archive.pages.dev/mcp`), or run the local stdio server via `npx rbi-doc-mcp --local`. Both give instant access to BM25F search, circular reference resolution, point-in-time validity verification, and full Markdown retrieval.

### How does `npx rbi-doc-mcp --local` work offline or without hitting rate limits?
When you run `npx rbi-doc-mcp --local`, the CLI downloads only the compact static index shards needed for your query from `https://rbi-archive.pages.dev/idx/v2` and caches them on disk under `~/.cache/rbi-doc-mcp/idx-v2`. Full Markdown documents are fetched directly from the public GitHub Raw (`raw.githubusercontent.com/imsovikde/rbi-regulatory-archive-1991-2026`) and Hugging Face dataset mirrors.

### What should I do if I receive HTTP `429 Too Many Requests`?
Wait for the number of seconds indicated in the `Retry-After` response header, sign in with a free account at `https://rbi-archive.pages.dev/account` to quadruple your allowance from 30 to 120 requests/minute, batch multi-hop lookups into a single call using `rbi_doc_execute_code`, or switch to `npx rbi-doc-mcp --local` for unlimited local execution.

### How do I revoke an active MCP client session?
Sign in at `https://rbi-archive.pages.dev/account`, locate the connected client under **Active Sessions**, and click **Revoke** (or **Sign Out Everywhere** to invalidate all active tokens immediately).

---

## 7. Privacy Notice

The RBI Regulatory Archive processes only the minimum telemetry required for rate limiting, abuse protection, and your personal usage dashboard:
- Client IP addresses are never stored in raw form; rate-limit buckets use a daily-rotated SHA-256 salted hash that cannot be reversed.
- Account passwords are derived using PBKDF2-HMAC-SHA256 (600,000 iterations) plus an HMAC pepper before storage.
- Search query strings and OAuth authorization codes are stripped from operational logs.
- You can inspect and revoke all active sessions at any time from `https://rbi-archive.pages.dev/account`.
