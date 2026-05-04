"""Standalone MCP server exposing Qogen tools.

Run with: uv run python -m qogen.mcp_server
Or write into Claude Code via .mcp.json (see REAMME).
"""

from mcp.server.fastmcp import FastMCP
import httpx
from qogen.doc_builder import build_one_pager

mcp = FastMCP("qogen")

@mcp.tool()
def generate_one_pager(
    product_name: str,
    tagline: str,
    features: list[str],
    audience: str,
    body_copy: str,
) -> str:
    """ Generate a branded one-page marketing document (.docx).
    Returns the absolute file path of the generated document.
    """

    return build_one_pager(
        product_name=product_name,
        tagline=tagline,
        features=features,
        audience=audience,
        body_copy=body_copy,
    )

@mcp.tool()
def lookup_competitor(name: str) -> str:
    """Look up a brief summary of a company or product via wikipedia."""
    url= f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    try:
        r = httpx.get(url, headers={"User-Agent": "Qogen/0.1"}, timeout=10)
        r.raise_for_status()
        return r.json().get("extract", "No summary avalaible.")
    except Exception as e:
        return f"Lookup failed: {e}"
    

if __name__ == "__main__":
    mcp.run()