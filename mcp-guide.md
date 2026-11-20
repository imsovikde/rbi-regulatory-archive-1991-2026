# RBI Regulatory Archive: Model Context Protocol (MCP) & Web Portal Guide

This guide covers connecting AI assistants, code editors, and custom HTTP clients to the Reserve Bank of India (RBI) Regulatory Archive (1991 to 2026, 88,236 documents) over the Model Context Protocol (MCP), as well as managing your account and sessions on the public web portal.

## 1. Official Endpoints

| Surface | URL | Purpose |
| :--- | :--- | :--- |
| Public Web Portal & Terminal | `https://rbi-archive.pages.dev` | Interactive document search, statutory graph explorer, validity verifier, and court citation generator |
| Official MCP Endpoint | `https://rbi-archive.pages.dev/mcp` | Streamable HTTP (MCP 2025-06-18) and JSON-RPC 2.0 endpoint for AI agents |
| User Account & Usage Dashboard | `https://rbi-archive.pages.dev/account` | Usage metrics, active OAuth sessions, tool breakdown, and session revocation |
| Sign In / Sign Up | `https://rbi-archive.pages.dev/auth/signin` | Direct browser sign-in, account creation, and one-click anonymous session start |
| OAuth 2.1 Protected Resource Metadata | `https://rbi-archive.pages.dev/.well-known/oauth-protected-resource` | RFC 9728 resource discovery for MCP clients |
| OAuth 2.1 Authorization Server Metadata | `https://rbi-archive.pages.dev/.well-known/oauth-authorization-server` | RFC 8414 OAuth 2.1 + PKCE (`S256`) and Dynamic Client Registration discovery |

## 2. Step-by-Step Client Setup

### Claude Code (CLI)

Connect Claude Code directly to the Streamable HTTP endpoint:

```bash
claude mcp add --transport http rbi-archive https://rbi-archive.pages.dev/mcp
```

When prompted for authentication, you can either authorize through the browser (OAuth 2.1 with PKCE) or select anonymous public access for immediate read-only queries.

### Claude (Web & Desktop Custom Connectors)

1. Open Claude Settings and navigate to **Connectors** (or **Integrations**).
2. Click **Add Custom Connector**.
3. Set the name to `RBI Regulatory Archive` and the Server URL to:
   ```text
   https://rbi-archive.pages.dev/mcp
   ```
4. When the OAuth consent window opens at `https://rbi-archive.pages.dev/oauth/authorize`, choose one of three options:
   - **Sign In**: Enter your registered email and password.
   - **Create Account**: Register a free account with email and password.
   - **Continue Anonymously**: Authorize a read-only session immediately without creating an account.

If you configure Claude Desktop via `claude_desktop_config.json` (`%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "rbi-archive": {
      "url": "https://rbi-archive.pages.dev/mcp"
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
    }
  }
}
```

Open Cursor Settings > **MCP** to confirm the `rbi-archive` server appears with its 8 tools enabled. If prompted to sign in, complete the browser flow or click **Continue Anonymously**.

### VS Code / GitHub Copilot

Add the server to `.vscode/mcp.json` in your workspace (or your user `settings.json` under `mcp.servers`):

```json
{
  "servers": {
    "rbi-archive": {
      "type": "http",
      "url": "https://rbi-archive.pages.dev/mcp"
    }
  }
}
```

In GitHub Copilot Chat, switch to **Agent** mode and select the `rbi-archive` tools from the tool picker.

### Windsurf

Open Windsurf MCP settings (`~/.codeium/windsurf/mcp_config.json`) and add:

```json
{
  "mcpServers": {
    "rbi-archive": {
      "serverUrl": "https://rbi-archive.pages.dev/mcp"
    }
  }
}
```

### Generic Streamable HTTP MCP Clients (cURL / Python / TypeScript)

Any MCP client supporting Streamable HTTP (`POST https://rbi-archive.pages.dev/mcp` with `Content-Type: application/json`) can call the server directly without prior authentication headers under the public tier, or pass an OAuth 2.1 Bearer token (`Authorization: Bearer <access_token>`) obtained via PKCE.

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

## 3. Account & Access Tiers

All users can access the full 88,236-document archive at zero cost. Two access tiers are available:

| Feature | Continue Anonymously (`anonymous`) | Free Registered Account (`registered`) |
| :--- | :--- | :--- |
| Cost | Free | Free |
| Sign-up required | None (one-click or zero-header HTTP) | Email + password (10 to 128 characters) |
| Rate limit | 30 requests / minute | 120 requests / minute |
| Granted OAuth scopes | `rbi:read` | `rbi:read rbi:code_mode` |
| Read-only statutory & search tools (7 tools) | Enabled | Enabled |
| Multi-step Code Mode (`rbi_doc_execute_code`) | Disabled (or capped on unauthenticated HTTP) | Full access |
| Usage dashboard & session management | Session-scoped view at `/account` | Persistent usage history, 7-day activity chart, per-tool breakdown, and individual session revocation at `https://rbi-archive.pages.dev/account` |

To create or manage a free account, visit `https://rbi-archive.pages.dev/account` or `https://rbi-archive.pages.dev/auth/signup`. From the dashboard you can update your display name, inspect your 24-hour, 7-day, and 30-day tool call counts, see which MCP clients are connected, and revoke individual OAuth sessions or sign out everywhere.

## 4. Public Tool Reference & Example Prompts

The MCP server exposes 8 public tools.

### 4.1 `search_rbi_regulations`

Hybrid BM25F (`k1 = 1.2`, `b = 0.75`) and 128-dim semantic search across all 88,236 RBI Master Directions, Circulars, Notifications, Draft Guidelines, and Press Releases (1991 to 2026) with validity-prior modulation.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | Yes | Search keywords, circular subject, or regulatory concept |
| `limit` | `number` | No | Maximum results to return (default `5`, max `20`) |
| `category` | `string` | No | Filter by `Master-Directions`, `Master-Circulars`, `Circulars`, `Notifications`, `Draft-Notifications-Guidelines`, or `Press-Releases` |
| `year` | `number` | No | Filter by publication year (`1991` to `2026`) |
| `statute` | `string` | No | Filter by governing statute (`BR_ACT_1949`, `RBI_ACT_1934`, `FEMA_1999`, `PMLA_2002`, `PSS_ACT_2007`, `SARFAESI_2002`) |

**Example prompt:**
> "Search RBI Master Directions and Circulars for digital lending default loss guarantee (FLDG) limits and list the top 5 controlling documents with their circular numbers."

### 4.2 `fetch_rbi_markdown`

Retrieves the verified GitHub-Flavored Markdown text of any RBI regulatory document by its canonical `doc_id`, with optional section filtering and SHA-256 provenance metadata.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical numeric or slug document ID returned by `search_rbi_regulations` or `resolve_rbi_doc` |
| `section` | `string` | No | Optional heading or section filter (for example, `Applicability`, `Definitions`, `Penalties`) |

**Example prompt:**
> "Fetch the full markdown text of RBI document `MD_106` (Master Direction on Digital Payment Security Controls) and extract the multi-factor authentication requirements."

### 4.3 `resolve_rbi_doc`

Resolves an RBI circular reference number (`RBI/2024-25/...`, `DOR.No...`, `DBOD.No...`), notification number, RBI URL (`?Id=13143`), or title fragment into its canonical `doc_id`, publication date, category, SHA-256 hash, and archive path.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `identifier` | `string` | Yes | Circular reference number, notification number, numeric ID, RBI URL, or title fragment |

**Example prompt:**
> "Resolve RBI circular reference `RBI/2015-16/100` (or numeric ID `13143`) into its canonical document ID, title, and archive links."

### 4.4 `trace_statutory_consequences`

Traces the causal statutory graph (`SUPERSEDES`, `AMENDS`, `REPEALS`, `CITES`) for a document, along with linked statutory penalties (such as Section 47A(1)(c) of the Banking Regulation Act, 1949) and mandatory compliance turnaround times (TATs).

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical document ID to trace across the statutory DAG |

**Example prompt:**
> "Trace the statutory consequences, amendment chain, and reporting turnaround times for RBI document `13143`."

### 4.5 `verify_circular_validity`

Evaluates point-in-time legal validity (`ACTIVE`, `SUPERSEDED`, or `REPEALED`) for any circular on a given `YYYY-MM-DD` date by traversing incoming supersession and repeal edges in the statutory DAG.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `doc_id` | `string` | Yes | Canonical document ID to check |
| `as_of_date` | `string` | No | ISO calendar date (`YYYY-MM-DD`); defaults to today |

**Example prompt:**
> "Verify whether RBI circular `13143` was legally in force on `2022-06-30` and on `2026-01-15`, and identify any superseding circular."

### 4.6 `format_court_citation`

Generates a formal judicial citation string suitable for Supreme Court of India, High Court, NCLAT, and regulatory compliance filings, complete with the official RBI reference number, date, statutory authority, and SHA-256 verification digest.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `identifier` | `string` | Yes | Canonical `doc_id` or official RBI circular number |

**Example prompt:**
> "Format a court-ready legal citation with SHA-256 verification hash for RBI document `13143`."

### 4.7 `rag_query_rbi_provisions`

Performs clause-level retrieval-augmented generation (RAG) over Content-Defined Chunked (CDC) statutory provisions, returning the highest-scoring passages with exact document citations and section headers.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | Yes | Natural-language compliance question or statutory provision query |
| `top_k` | `number` | No | Number of provision chunks to retrieve (default `5`, max `15`) |
| `category` | `string` | No | Optional category filter |
| `year` | `number` | No | Optional year filter |

**Example prompt:**
> "Retrieve the exact RBI statutory provisions governing Video-based Customer Identification Process (V-CIP) audit trails and concurrent auditor verification under the KYC Master Direction."

### 4.8 `rbi_doc_execute_code`

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

## 5. Troubleshooting & Privacy

### Handling HTTP 429 Rate Limits

If your client exceeds its per-minute allowance (30 requests/minute for anonymous sessions or 120 requests/minute for registered accounts) or the daily service protection ceiling, the server returns HTTP `429 Too Many Requests` with a `Retry-After` header in seconds and a JSON body describing the active limit. Wait for the `Retry-After` interval before retrying, or sign in with a free account at `https://rbi-archive.pages.dev/account` to raise your allowance to 120 requests/minute and batch multi-step lookups with `rbi_doc_execute_code`.

### Re-Authorizing Expired or Revoked Sessions

OAuth 2.1 access tokens expire after 30 minutes and automatically rotate via 7-day refresh tokens. If you revoke a session from `https://rbi-archive.pages.dev/account` or your refresh token expires, your MCP client will receive HTTP `401 Unauthorized` with a `WWW-Authenticate` header pointing to `https://rbi-archive.pages.dev/.well-known/oauth-protected-resource`. Reconnect or toggle the server in your MCP client to trigger a fresh browser authorization flow.

### Privacy Notice

The RBI Regulatory Archive processes only the minimum telemetry required for rate limiting, abuse prevention, and your personal usage dashboard:
- Client IP addresses are never stored in raw form; rate-limit buckets use a daily-rotated SHA-256 salted hash that cannot be reversed.
- Account passwords are derived client-side and server-side using PBKDF2-HMAC-SHA256 (600,000 iterations) plus an HMAC pepper before storage.
- Search query strings and OAuth authorization codes are stripped from operational logs.
- You can inspect and revoke all active sessions at any time from `https://rbi-archive.pages.dev/account`, or review the Privacy Notice on `https://rbi-archive.pages.dev`.
