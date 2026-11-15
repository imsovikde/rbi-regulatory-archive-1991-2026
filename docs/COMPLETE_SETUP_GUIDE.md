# Complete Setup and Integration Guide: RBI Regulatory Model Context Protocol

Author: Souvik Dey (imsovikde@gmail.com)  
Version: 1.0.0  
Canonical MCP Endpoint: `https://rbi-doc-mcp.imsovikde.workers.dev/mcp`  
Documentation Repository: https://github.com/imsovikde/rbi-doc-mcp  
Upstream Regulatory Archive: https://github.com/imsovikde/rbi-regulatory-archive-1991-2026  

---

## 1. System Architecture and Endpoint Routing

The Reserve Bank of India (RBI) Regulatory Model Context Protocol (MCP) server provides AI agents and applications with direct access to all 88,236 regulatory circulars, master directions, notifications, penalty orders, and compliance timelines published between 1991 and 2026.

The server operates on Cloudflare Workers backed by Cloudflare D1 (SQLite FTS5 full-text search) and Cloudflare R2 object storage.

### Endpoint Routing Architecture

1. Canonical MCP Endpoint: `/mcp` (e.g. `https://rbi-doc-mcp.imsovikde.workers.dev/mcp`)
   - Handles standard Model Context Protocol JSON-RPC 2.0 requests via HTTP POST (`initialize`, `tools/list`, `tools/call`).
   - Handles Server-Sent Events (SSE) connections via HTTP GET when the client sends `Accept: text/event-stream`.
   - Handles diagnostic schema discovery via HTTP GET, returning available tools and protocol version.
2. Root Route: `/` (e.g. `https://rbi-doc-mcp.imsovikde.workers.dev/`)
   - Reserved for the future web portal homepage. Currently returns service routing metadata pointing to `/mcp`.
3. Health Check: `/health`
   - Returns JSON status confirming D1 database connection, R2 storage bindings, and active execution planes.

---

## 2. Public Zero-Setup Tier: Instant Access Without Authentication

Anyone can query the MCP server immediately without an API key, credit card, or user registration.

### How the Public Tier Works
- Header requirement: None.
- Authentication method: Open anonymous access.
- Rate limit: 60 requests per minute per IP address.
- Burst allowance: Up to 60 requests before throttling begins.
- Use cases: Local agent execution, development, ad-hoc research, and command-line experimentation.

When an unauthenticated request arrives at `/mcp`, the edge worker checks the client IP against an in-memory token bucket. If the bucket has remaining tokens, the request processes with sub-50ms latency. If the limit is exceeded, the server returns HTTP 429 with a `Retry-After` header indicating how many seconds to wait before retrying.

---

## 3. Claude Code Integration

Claude Code supports remote MCP servers over HTTP POST. You can configure the server with or without authentication.

### Option A: Public Tier (No Authentication Required)

Run this command in your terminal:

```bash
claude mcp add rbi-doc-mcp https://rbi-doc-mcp.imsovikde.workers.dev/mcp
```

Claude Code connects to the endpoint, runs protocol handshake, lists available tools, and makes them accessible in your chat sessions.

### Option B: Authenticated Tier (API Key or Token)

If you have an enterprise API key or access token, pass it via headers during registration:

```bash
claude mcp add rbi-doc-mcp https://rbi-doc-mcp.imsovikde.workers.dev/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

### Option C: Manual Configuration File

Alternatively, add the server directly to your project or user configuration file (`~/.claude/config.json`):

```json
{
  "mcpServers": {
    "rbi-doc-mcp": {
      "url": "https://rbi-doc-mcp.imsovikde.workers.dev/mcp",
      "headers": {
        "User-Agent": "claude-code-client/1.0"
      }
    }
  }
}
```

---

## 4. Claude Desktop and Cursor Integration

### Claude Desktop

Edit your `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "rbi-doc-mcp": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp"],
      "env": {
        "RBI_DOC_MCP_URL": "https://rbi-doc-mcp.imsovikde.workers.dev/mcp"
      }
    }
  }
}
```

If connecting with an API key, add `RBI_DOC_MCP_API_KEY` to the `env` object:

```json
{
  "mcpServers": {
    "rbi-doc-mcp": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp"],
      "env": {
        "RBI_DOC_MCP_URL": "https://rbi-doc-mcp.imsovikde.workers.dev/mcp",
        "RBI_DOC_MCP_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Cursor IDE

Create or edit `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "rbi-doc-mcp": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp"],
      "env": {
        "RBI_DOC_MCP_URL": "https://rbi-doc-mcp.imsovikde.workers.dev/mcp"
      }
    }
  }
}
```

---

## 5. OAuth 2.1 PKCE Authentication Flow and UI Login Screen

For multi-tenant web applications, mobile apps, and developer portals, the MCP server supports OAuth 2.1 authorization with Proof Key for Code Exchange (PKCE). This eliminates static API keys and protects client secrets from exposure.

### Step 1: Client Generates PKCE Parameters

Before initiating authentication, the client generates a high-entropy cryptographic random string called the `code_verifier` (43 to 128 characters) and derives the `code_challenge`:

$$\text{code\_challenge} = \text{base64url}(\text{SHA256}(\text{code\_verifier}))$$

### Step 2: User Redirect to UI Login Screen

The client directs the user's browser to the authorization endpoint:

```
https://auth.rbi-doc.imsovikde.workers.dev/authorize?
  response_type=code
  &client_id=your-client-id
  &redirect_uri=https://your-app.com/callback
  &scope=rbi:read
  &state=random-security-token
  &code_challenge=E9Melhoa2OwvFrGMTJguCH5rtx64ZnAqEs9QCAr3349
  &code_challenge_method=S256
```

### Step 3: Interactive Login Screen Experience

The browser opens a clean authentication interface:
1. The user enters their institutional credentials or authenticates via Single Sign-On (SSO).
2. The screen displays requested scopes: "Read RBI regulatory documents, query compliance graph, access Code Mode SDK".
3. The user approves access.
4. The authorization server generates an authorization code bound strictly to the `client_id` and `code_challenge`.
5. The browser redirects back to `https://your-app.com/callback?code=AUTH_CODE_HERE&state=random-security-token`.

### Step 4: Token Exchange

Your backend exchanges the authorization code for tokens via HTTP POST:

```bash
curl -X POST https://auth.rbi-doc.imsovikde.workers.dev/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=your-client-id" \
  -d "code=AUTH_CODE_HERE" \
  -d "redirect_uri=https://your-app.com/callback" \
  -d "code_verifier=HIGH_ENTROPY_CODE_VERIFIER"
```

The authorization server verifies that $\text{SHA256}(\text{code\_verifier}) == \text{code\_challenge}$. If valid, it returns:

```json
{
  "access_token": "oauth_pkce_eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "rt_8f92a10b4...",
  "scope": "rbi:read"
}
```

### Step 5: Calling the MCP Endpoint with OAuth Token

Pass the access token in the `Authorization` header on all requests to `/mcp`:

```bash
curl -X POST https://rbi-doc-mcp.imsovikde.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer oauth_pkce_eyJhbGciOi..." \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"resolve_rbi_doc","arguments":{"identifier":"13143"}}}'
```

---

## 6. Enterprise Zero-Trust Authentication (Cloudflare Access)

For regulated banks, non-banking financial companies (NBFCs), and institutional audit systems, the MCP server integrates with Cloudflare Zero Trust.

### Service Token Headers

Automated microservices authenticate using Cloudflare Access Service Tokens:

```http
POST /mcp HTTP/1.1
Host: rbi-doc-mcp.imsovikde.workers.dev
Content-Type: application/json
CF-Access-Client-Id: 5491f092b67841e5927892.access
CF-Access-Client-Secret: c829401bfd9283749812739487291837498172938471
```

### Security Benefits
- Edge verification: Validated at the Cloudflare network layer before reaching the worker logic.
- Automated revocation: Revoke access instantly from Cloudflare Zero Trust dashboard without changing application code.
- Higher quota: Dedicated rate allowance of 10,000 requests per minute.

---

## 7. Rate Limiting Mathematics and Client Optimization

The server enforces continuous token bucket rate limiting:
- Public Tier: 60 requests/minute (refill rate: 1.0 token/second).
- Authenticated Tier: 5,000 requests/minute (refill rate: 83.33 tokens/second).
- Enterprise Service Tokens: 10,000 requests/minute (refill rate: 166.67 tokens/second).

### Client-Side Backoff and Retry Implementation

When making high-volume queries, clients should inspect the HTTP status code. If an HTTP 429 response occurs, read the `Retry-After` header and apply exponential backoff with full jitter:

$$t_{\text{sleep}} = \min(t_{\max}, \ 2^{\text{attempt}} \cdot t_{\text{base}}) \cdot \text{Uniform}(0.5, 1.5)$$

#### Python Example with Automated Retry

```python
import time
import json
import random
import urllib.request
import urllib.error

ENDPOINT = "https://rbi-doc-mcp.imsovikde.workers.dev/mcp"

def call_mcp_tool_safe(name: str, arguments: dict, api_key: str = None, max_retries: int = 4):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments}
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "rbi-client/1.0"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                ENDPOINT,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return json.loads(data["result"]["content"][0]["text"])
        except urllib.error.HTTPError as err:
            if err.code == 429:
                retry_after = int(err.headers.get("Retry-After", "2"))
                jitter = random.uniform(0.1, 0.5)
                sleep_duration = retry_after + jitter
                print(f"Rate limit reached. Sleeping {sleep_duration:.2f}s before retry {attempt+1}/{max_retries}")
                time.sleep(sleep_duration)
            else:
                raise err
    raise RuntimeError("Exceeded maximum retries for MCP request")
```

---

## 8. Complete MCP Tools Reference

The server exposes two execution planes:

### Plane 1: Cloudflare Code Mode (Token Budget < 900 Tokens)

Code Mode allows LLMs to write sandboxed JavaScript code that executes at the Cloudflare edge. The agent queries, filters, joins, and aggregates regulatory data across multiple tables in a single round-trip, returning only the synthesized final answer.

1. `rbi_doc_search_api`
   - Purpose: Discovers available methods, parameters, and type interfaces in the virtual `RbiDocSDK`.
   - Arguments: `query` (optional string, e.g. "search", "validity", "citation").
2. `rbi_doc_execute_code`
   - Purpose: Executes a sandboxed JavaScript code block against the edge database.
   - Arguments: `code` (string containing async JavaScript).
   - Example code argument:
     ```javascript
     const docs = await sdk.search({ query: "Know Your Customer", limit: 3 });
     const validity = await sdk.checkValidity(docs[0]?.doc_id || "");
     return { title: docs[0]?.title, status: validity.status };
     ```

### Plane 2: Direct Canonical MCP Tools

1. `resolve_rbi_doc`
   - Purpose: Resolves circular identifiers, notification numbers, numeric IDs (`?Id=13143`), or title fragments into canonical metadata, dates, and archive links.
   - Arguments: `identifier` (string, required).
2. `search_rbi_regulations`
   - Purpose: Sub-50ms hybrid FTS5 search across all 88,236 documents.
   - Arguments:
     - `query` (string, required)
     - `limit` (number, default: 5, max: 20)
     - `category` (string, optional: "circulars", "notifications", "master-directions", "press-releases")
     - `year` (number, optional, e.g. 2024)
     - `statute` (string, optional: "BR_ACT_1949", "RBI_ACT_1934", "FEMA_1999", "PMLA_2002")
3. `fetch_rbi_markdown`
   - Purpose: Downloads the full text markdown of any regulation from the archive with optional section extraction.
   - Arguments:
     - `doc_id` (string, required)
     - `section` (string, optional, e.g. "Penalties", "Applicability")
4. `trace_statutory_consequences`
   - Purpose: Traces causal amendment chains, parent Master Directions, Section 47A penalty ledgers, and turnaround times (TAT).
   - Arguments: `doc_id` (string, required).
5. `verify_circular_validity`
   - Purpose: Verifies whether a circular was legally in force on a given calendar date, reporting `ACTIVE`, `SUPERSEDED`, or `REPEALED`.
   - Arguments:
     - `doc_id` (string, required)
     - `as_of_date` (string, optional, format: `YYYY-MM-DD`, defaults to current date)
6. `format_court_citation`
   - Purpose: Formats standard Indian legal citation strings for Supreme Court, High Court, and regulatory filings with SHA-256 verification hash.
   - Arguments: `identifier` (string, required).

---

## 9. Verification and Testing

Verify your integration with a single curl command:

```bash
curl -X POST https://rbi-doc-mcp.imsovikde.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -H "User-Agent: rbi-test/1.0" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "verify_circular_validity",
      "arguments": {
        "doc_id": "13143",
        "as_of_date": "2026-11-15"
      }
    }
  }'
```

Expected response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\n  \"doc_id\": \"13143\",\n  \"status\": \"ACTIVE\",\n  \"as_of_date\": \"2026-11-15\"\n}"
      }
    ]
  }
}
```
