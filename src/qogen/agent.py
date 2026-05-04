"""Claude Agent SDK loop for QoGen"""

import anyio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
)
from rich.console import Console
from qogen.tools import generate_one_pager_tool, lookup_competitor_tool

console = Console()

SYSTEM_PROMPT = """You are Qogen, a marketing automation assistant

When given a product brief:

1. If the brief mentions competitors or a market space, call lookup_competitor
to gather brief context (max 1-2 lookups).
2. Then call generate_one_pager with strong, specific marketing copy.

Be concise. Generate clear, benefit-driven copy. Avoid corporate jargon
"""

async def run_agent(brief: str) -> None:
    server = create_sdk_mcp_server(
        name="qogen",
        version="01.0",
        tools=[generate_one_pager_tool, lookup_competitor_tool],
    )

    options = ClaudeAgentOptions(
        mcp_servers={"qogen": server},
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=[
            "mcp__qogen__generate_one_pager",
            "mcp__qogen__lookup_competitor",
        ],
        max_turns=8,
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(brief)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        console.print(f"[cyan]Claude:[/cyan] {block.text}")

    
def main(brief: str) -> None:
    anyio.run(run_agent, brief)
