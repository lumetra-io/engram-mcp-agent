"""
engram_mcp_agent — Engram MCP server wiring for the lastmile-ai mcp-agent framework.

`mcp-agent` is an agent framework that consumes MCP servers as the tool layer.
Engram already exposes an MCP endpoint, so wiring is a single MCPServerSettings
entry. This module provides a helper that returns the right settings.

Usage:

    from mcp_agent.app import MCPApp
    from mcp_agent.config import Settings, MCPSettings
    from mcp_agent.agents.agent import Agent
    from engram_mcp_agent import engram_server_settings

    app = MCPApp(
        name="my-app",
        settings=Settings(
            mcp=MCPSettings(servers={"engram": engram_server_settings()}),
            # ...your other settings (LLM provider, etc.)
        ),
    )

    async with app.run() as running:
        agent = Agent(
            name="researcher",
            instruction="Use engram to remember and recall facts.",
            server_names=["engram"],
        )
"""

from __future__ import annotations

import os
from typing import Optional

from mcp_agent.config import MCPServerSettings


def engram_server_settings(
    *,
    api_key: Optional[str] = None,
    url: str = "https://mcp.lumetra.io/mcp/sse",
) -> MCPServerSettings:
    """Return an MCPServerSettings for the hosted Engram MCP server.

    `api_key` defaults to the ENGRAM_API_KEY environment variable. The
    transport is SSE (Engram's native MCP transport).
    """
    key = api_key or os.environ.get("ENGRAM_API_KEY")
    if not key:
        raise ValueError(
            "Engram API key required. Pass api_key=... or set ENGRAM_API_KEY in the environment."
        )
    return MCPServerSettings(
        name="engram",
        description="Lumetra Engram — durable, explainable memory for AI agents.",
        transport="sse",
        url=url,
        headers={"Authorization": f"Bearer {key}"},
    )
