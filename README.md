# engram-mcp-agent

[mcp-agent](https://github.com/lastmile-ai/mcp-agent) integration for [Engram](https://lumetra.io) — one-line MCP server wiring so any mcp-agent app can use Engram as its memory layer.

`mcp-agent` is an MCP-first agent framework: agents consume MCP servers as their tool layer. Engram already exposes an MCP endpoint, so the entire integration is a single `MCPServerSettings` entry. This module returns it pre-configured.

## Install

```bash
pip install lumetra-engram mcp-agent
```

Vendor `engram_mcp_agent.py` from this repo (~30 LOC). PyPI release coming.

```bash
export ENGRAM_API_KEY="eng_live_..."
```

## Get an Engram API key

Sign up at <https://lumetra.io> — free tier, no card. You'll see an `eng_live_…` token in your dashboard.

**Don't forget BYOK** — Engram is bring-your-own-key end-to-end for the LLM that does extraction + synthesis. Configure a provider at <https://lumetra.io/models>. DeepSeek is cheap and fast. Without one, store/query returns HTTP 412.

## Usage

```python
from mcp_agent.app import MCPApp
from mcp_agent.config import Settings, MCPSettings
from mcp_agent.agents.agent import Agent
from engram_mcp_agent import engram_server_settings

app = MCPApp(
    name="my-app",
    settings=Settings(
        mcp=MCPSettings(servers={"engram": engram_server_settings()}),
        # ...your LLM provider config, other servers, etc.
    ),
)

async with app.run() as running:
    agent = Agent(
        name="researcher",
        instruction="Use the engram server to remember and recall facts across sessions.",
        server_names=["engram"],
    )
```

The agent now has all six native Engram MCP tools — `store_memory`, `query_memory`, `list_memories`, `list_buckets`, `delete_memory`, `clear_memories` — wired through mcp-agent's standard tool-routing layer.

## Why this integration is so small

mcp-agent is MCP-native, and Engram already exposes an MCP endpoint. The integration is a single `MCPServerSettings` entry — no adapter code, no tool wrappers, no schema mapping. The agent's tool surface comes straight from MCP discovery.

## Verified

Smoke-tested against live `api.lumetra.io`:

- `engram_server_settings()` returns a valid `MCPServerSettings` with `transport="sse"`, the correct URL, and `Authorization: Bearer <key>` header populated.
- The same Bearer token reaches Engram's HTTP API and returns the tenant's bucket list, confirming the credentials and transport choice work end-to-end.

For a full agent-loop verification, drop the helper into the standard mcp-agent starter and run any of their example workflows; Engram appears as the `engram` server in `agent.server_names` and the six tools are immediately available.

## License

MIT — Lumetra
