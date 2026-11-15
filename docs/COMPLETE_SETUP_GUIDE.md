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
   - Case-insensitive routing: both `/mcp` and `/MCP` route to the same handler.
2. Root Route: `/` (e.g. `https://rbi-doc-mcp.imsovikde.workers.dev/`)
   - Reserved for the future web portal homepage. Currently returns service routing metadata pointing clients to `/mcp`.
3. Health Check: `/health`
   - Returns JSON status confirming D1 database connection, R2 storage bindings, and active execution planes.

---

## 2. Public Zero-Setup Tier: Instant Access Without Any Signup

Anyone can query the MCP server immediately without an account, credit card, or API key.

### How Public Access Operates
- Header requirement: None.
- Sign-up requirement: None.
- Rate limit: 60 requests per minute per IP address.
- Burst allowance: Up to 60 requests instantaneously before throttling begins.
- Use cases: Local agent execution, developer experimentation, rapid statutory lookups, and ad-hoc compliance checks.

When an unauthenticated request arrives at `/mcp`, the edge worker inspects the client IP address against an in-memory token bucket. If the bucket has tokens remaining, the request processes with sub-50ms latency. If the limit is exceeded, the server returns HTTP 429 with a `Retry-After` header indicating how many seconds to wait before retrying.

### Rate Limit Optimization for Public Users: Code Mode

In standard MCP tool calling, an agent answering a complex question might make 5 to 10 sequential round-trips:
1. Search documents
2. Retrieve text
3. Trace statutory amendments
4. Check point-in-time validity
5. Format citation

Under the public rate limit of 60 requests per minute, making 10 individual calls for a single query consumes 10 tokens.

To optimize token consumption, public users can use Plane 1 Code Mode (`rbi_doc_execute_code`). The agent sends a single JavaScript snippet that executes all database queries, joins, and filtering inside the Cloudflare edge node in a single request. The entire multi-hop lookup consumes **only 1 token**, allowing users to perform dozens of complex legal research tasks without hitting limits.

---

## 3. Claude Code Integration: Step-by-Step Walkthrough

Claude Code supports remote MCP servers over HTTP POST.

### Scenario A: You Do Not Have an Account (Public Zero-Setup Mode)

If you do not have an account, do not want to register, and just want the server to work immediately:

#### Method 1: Single Terminal Command

Run this command in your terminal:

```bash
claude mcp add rbi-doc-mcp https://rbi-doc-mcp.imsovikde.workers.dev/mcp
```

Claude Code connects to `https://rbi-doc-mcp.imsovikde.workers.dev/mcp`, performs the MCP `initialize` handshake, retrieves the list of 8 tools, and configures the server.

#### Method 2: Interactive Terminal Wizard

If you run `claude mcp add` without inline flags, Claude Code prompts:

```text
Enter MCP server name: rbi-doc-mcp
Enter server URL: https://rbi-doc-mcp.imsovikde.workers.dev/mcp
Choose authentication method:
  > [1] None / Public (No authentication required)
    [2] HTTP Bearer Token
    [3] OAuth 2.0 / 2.1
    [4] Custom Headers
```

**What option to choose:** Select **`[1] None / Public`**.
No username, password, or API key is required. Claude Code stores the configuration and connects immediately under the public rate limit.

#### Method 3: Manual Configuration File

Alternatively, add the server directly to `~/.claude/config.json`:

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

### Scenario B: Authenticated Access (API Key or Cloudflare Access)

If you have an enterprise API key or Cloudflare Access credentials:

```bash
claude mcp add rbi-doc-mcp https://rbi-doc-mcp.imsovikde.workers.dev/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

For Cloudflare Access Zero Trust service tokens:

```bash
claude mcp add rbi-doc-mcp https://rbi-doc-mcp.imsovikde.workers.dev/mcp \
  --header "CF-Access-Client-Id: YOUR_CLIENT_ID" \
  --header "CF-Access-Client-Secret: YOUR_CLIENT_SECRET"
```

---

## 4. Claude Desktop and Cursor IDE Integration

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

If connecting with an enterprise API key, add `RBI_DOC_MCP_API_KEY`:

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

## 5. OAuth 2.1 PKCE Flow and Interactive Browser Login Screen

When higher throughput (5,000 requests/minute) or enterprise audit trails are needed, the server supports OAuth 2.1 with Proof Key for Code Exchange (PKCE).

### How the Interactive Login Screen Pops Up

1. **Client Initiation**:
   When an application initiates OAuth, it starts an ephemeral local callback listener on `http://localhost:PORT/callback` and generates a cryptographic `code_verifier` (a high-entropy random string) and `code_challenge`:
   $$\text{code\_challenge} = \text{base64url}(\text{SHA256}(\text{code\_verifier}))$$

2. **Browser Launch**:
   The terminal or application launches the system's default browser to the authorization URL:
   ```
   https://auth.rbi-doc.imsovikde.workers.dev/authorize?
     response_type=code
     &client_id=your-client-id
     &redirect_uri=http://localhost:PORT/callback
     &scope=rbi:read
     &code_challenge=E9Melhoa2OwvFrGMTJguCH5rtx64ZnAqEs9QCAr3349
     &code_challenge_method=S256
   ```

3. **Login Screen Visual Design**:
   The browser opens a clean, trust-first interface designed according to strict editorial principles:
   - Deep slate neutral canvas (`#090d16` background in dark mode, `#ffffff` in light mode).
   - Crisp typographic hierarchy using system sans-serif font stack.
   - 1px subtle borders (`#1e293b`), avoiding oversaturated gradients and generic glassmorphism.
   - Clear authentication options:
     - Single Sign-On (SAML 2.0 / OIDC) for banks, law firms, and regulated institutions.
     - GitHub / Google developer authentication.
     - Passkey / WebAuthn passwordless sign-in.
   - Clear disclosure of requested permissions: "Read-only access to RBI regulatory documents, causal amendment graphs, and penalty records (`rbi:read`)."

4. **Authorization and Callback**:
   When the user clicks "Authorize":
   - The authorization server validates credentials and creates an authorization code bound strictly to the `code_challenge`.
   - The browser redirects to `http://localhost:PORT/callback?code=AUTH_CODE_HERE`.
   - The local listener captures the code and immediately closes.
   - The browser tab displays: "Authentication successful. You may close this window and return to your terminal."

5. **Token Exchange**:
   The client exchanges the authorization code and `code_verifier` for tokens:
   ```bash
   curl -X POST https://auth.rbi-doc.imsovikde.workers.dev/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code" \
     -d "client_id=your-client-id" \
     -d "code=AUTH_CODE_HERE" \
     -d "redirect_uri=http://localhost:PORT/callback" \
     -d "code_verifier=HIGH_ENTROPY_CODE_VERIFIER"
   ```

6. **Automatic Background Refresh**:
   The authorization server returns an `access_token` (valid for 1 hour) and a `refresh_token` (valid for 30 days). The client automatically refreshes tokens in the background without prompting the user again.

---

## 6. Enterprise Zero-Trust (Cloudflare Access Service Tokens)

For headless servers, automated compliance monitors, and CI/CD pipelines, Cloudflare Zero Trust service tokens provide perimeter-level security.

### Service Token Request Format

Pass the credentials via HTTP request headers:

```http
POST /mcp HTTP/1.1
Host: rbi-doc-mcp.imsovikde.workers.dev
Content-Type: application/json
CF-Access-Client-Id: 5491f092b67841e5927892.access
CF-Access-Client-Secret: c829401bfd9283749812739487291837498172938471
```

### Operational Characteristics
- Edge validation: Validated by Cloudflare global network edge nodes before touching worker execution memory.
- Rate limit: 10,000 requests per minute.
- Revocation: Instant revocation via Cloudflare Zero Trust dashboard without code modifications.

---

## 7. Rate Limiting Mathematics and Client Optimization

The server enforces continuous token bucket rate limiting:
- Public Zero-Setup Tier: 60 requests/minute (refill rate: 1.0 token/second).
- Authenticated Tier: 5,000 requests/minute (refill rate: 83.33 tokens/second).
- Enterprise Service Tokens: 10,000 requests/minute (refill rate: 166.67 tokens/second).

### Client Backoff with Full Jitter

When building automated query loops, clients should inspect HTTP status codes. If an HTTP 429 response is encountered, read the `Retry-After` header and apply exponential backoff with full jitter:

$$t_{\text{sleep}} = \min(t_{\max}, \ 2^{\text{attempt}} \cdot t_{\text{base}}) \cdot \text{Uniform}(0.5, 1.5)$$

#### Python Client Implementation

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

The server exposes 8 canonical tools organized across two execution planes:

### Plane 1: Cloudflare Code Mode (Token Budget < 600 Tokens)

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

## 9. Verification Command

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
