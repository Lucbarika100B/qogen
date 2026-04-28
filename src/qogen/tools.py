"""Custom tools exposed to Claude via the Agent SDK."""
import httpx
from claude_agent_sdk import tool
from qogen.doc_builder import build_one_pager


@tool(
    "generate_one_pager",
    "Generate a branded one-page marketing document (.docx) from a product brief. "
    "Returns the absolute file path of the generated document.",
    {
        "product_name": str,
        "tagline": str,
        "features": list,
        "audience": str,
        "body_copy": str,
    },
)
async def generate_one_pager_tool(args):
    path = build_one_pager(
        product_name=args["product_name"],
        tagline=args["tagline"],
        features=args["features"],
        audience=args["audience"],
        body_copy=args["body_copy"],
    )
    return {
        "content": [
            {"type": "text", "text": f"Generated one-pager at: {path}"}
        ]
    }


@tool(
    "lookup_competitor",
    "Look up a brief summary of a company or product via Wikipedia. "
    "Use to research market context before writing marketing copy.",
    {"name": str},
)
async def lookup_competitor_tool(args):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{args['name']}"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(url, headers={"User-Agent": "Qogen/0.1"})
            r.raise_for_status()
            data = r.json()
            extract = data.get("extract", "No summary available.")
        except httpx.HTTPStatusError as e:
            extract = f"Lookup failed ({e.response.status_code}). Proceed without."
        except Exception as e:
            extract = f"Lookup error: {e}. Proceed without."
    return {"content": [{"type": "text", "text": extract}]}