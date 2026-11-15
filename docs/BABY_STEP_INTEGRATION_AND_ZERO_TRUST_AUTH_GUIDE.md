# Baby Step Integration and Zero Trust Authentication Guide: RBI DOC MCP

Author: Souvik Dey (imsovikde@gmail.com)  
Version: 1.0.0  
Live Endpoint: `https://rbi-doc-mcp.imsovikde.workers.dev`

---

## 1. Quick Overview

RBI DOC MCP connects AI agents and human developers to the entire Reserve Bank of India (RBI) Regulatory Archive (1991 to Present).

The server operates two execution planes:
1. Plane 1 (Cloudflare Code Mode): Dynamic tool discovery (<900 tokens) and sandboxed JavaScript execution (`rbi_doc_execute_code`) that runs multi-hop queries inside the Cloudflare edge without streaming large datasets back to the LLM.
2. Plane 2 (Canonical MCP Tools): Direct JSON-RPC tools for document resolution, search, markdown extraction, causal consequence tracing, point-in-time validity checking, and judicial citation formatting.

---

## 2. Zero-Trust Authentication Configuration

The server supports four authentication tiers depending on your security posture:

### Tier 1: Public Rate-Limited (Zero Setup)
- Header: None required.
- Rate Limit: 60 requests per minute per IP address.
- Use Case: Development, testing, ad-hoc queries, and local exploration.

### Tier 2: Bearer API Key
- Header: `Authorization: Bearer <RBI_DOC_MCP_API_KEY>`
- Rate Limit: 5,000 requests per minute.
- Use Case: Production microservices, CI/CD pipelines, and enterprise agent systems.

### Tier 3: Cloudflare Access Service Token (Zero-Trust Enterprise)
- Headers:
  - `CF-Access-Client-Id: <your-service-token-id>`
  - `CF-Access-Client-Secret: <your-service-token-secret>`
- Rate Limit: 10,000 requests per minute.
- Use Case: Regulated banking entities, automated security scanners, and zero-trust perimeter enforcement.

### Tier 4: OAuth 2.1 with PKCE
- Header: `Authorization: Bearer oauth_pkce_<session-token>`
- Rate Limit: 5,000 requests per minute.
- Use Case: Interactive multi-tenant user authentication flows.

---

## 3. Client Integration Recipes

### A. Claude Desktop Integration

Add the following to your `claude_desktop_config.json`:

On Windows: `%APPDATA%\Claude\claude_desktop_config.json`  
On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`  
On Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "rbi-doc-mcp": {
      "command": "npx",
      "args": ["-y", "rbi-doc-mcp"],
      "env": {
        "RBI_DOC_MCP_URL": "https://rbi-doc-mcp.imsovikde.workers.dev/mcp",
        "RBI_DOC_MCP_API_KEY": ""
      }
    }
  }
}
```

### B. Cursor IDE Integration

In your Cursor workspace root, create `.cursor/mcp.json`:

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

### C. Claude Code CLI

Add the server to Claude Code via terminal:

```bash
claude mcp add rbi-doc-mcp npx -y rbi-doc-mcp
```

Or configure in `~/.claude/config.json`:

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

### D. Python Integration (Gemini / OpenAI / Anthropic)

```python
import json
import urllib.request

class RbiDocClient:
    def __init__(self, endpoint="https://rbi-doc-mcp.imsovikde.workers.dev/mcp", api_key=None):
        self.endpoint = endpoint
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "rbi-doc-mcp-client/1.0.0"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def call_tool(self, name: str, args: dict):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": args}
        }
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=self.headers
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        return json.loads(data["result"]["content"][0]["text"])

# Example Usage:
client = RbiDocClient()

# 1. Search regulations
results = client.call_tool("search_rbi_regulations", {"query": "digital lending guidelines", "limit": 3})
print("Search results count:", len(results.get("results", [])))

# 2. Check circular validity
validity = client.call_tool("verify_circular_validity", {"doc_id": "13143", "as_of_date": "2026-11-15"})
print("Validity status:", validity.get("status"))

# 3. Format judicial citation
citation = client.call_tool("format_court_citation", {"identifier": "13143"})
print("Court citation:", citation.get("standard_citation"))
```

### E. TypeScript / Node.js Integration

```typescript
async function callRbiDocMcp(toolName: string, toolArgs: Record<string, any>) {
  const response = await fetch("https://rbi-doc-mcp.imsovikde.workers.dev/mcp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "User-Agent": "rbi-doc-mcp-client/1.0.0"
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: toolName,
        arguments: toolArgs
      }
    })
  });

  const data = await response.json();
  return JSON.parse(data.result.content[0].text);
}

// Example: Execute Code Mode Join
const codeResult = await callRbiDocMcp("rbi_doc_execute_code", {
  code: `
    const docs = await sdk.search({ query: "KYC", limit: 2 });
    const validity = await sdk.checkValidity(docs[0]?.doc_id || "");
    return { title: docs[0]?.title, validityStatus: validity.status };
  `
});
console.log(codeResult);
```

---

## 4. Canonical MCP Tools Reference

1. `rbi_doc_search_api`: Discovers methods, arguments, and type interfaces for Code Mode.
2. `rbi_doc_execute_code`: Executes sandboxed JavaScript queries against the virtual `RbiDocSDK`.
3. `resolve_rbi_doc`: Resolves any circular ID, notification number, or title fragment to metadata.
4. `search_rbi_regulations`: Fast hybrid FTS5 search with category, year, entity, and statute filters.
5. `fetch_rbi_markdown`: Downloads full markdown text with optional section heading filtering.
6. `trace_statutory_consequences`: Queries causal amendment chains, parent Master Directions, and Section 47A penalties.
7. `verify_circular_validity`: Verifies whether a circular was active, superseded, or repealed as-of date $T$.
8. `format_court_citation`: Formats Indian legal citation strings with content SHA-256 for court filings.
