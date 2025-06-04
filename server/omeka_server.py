import asyncio

import mcp.server.stdio
import mcp.types as mcptypes
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from server.omeka.client import OmekaClient
from server.omeka.tools import get_tools

server = Server("OmekaSMCP")
client = OmekaClient()


@server.list_tools()
async def handle_list_tools() -> list[mcptypes.Tool]:
    """利用可能なツールの一覧を返す"""
    return get_tools()


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[mcptypes.TextContent]:
    """ツール実行リクエストを処理"""
    if not arguments:
        arguments = {}

    try:
        if name == "list-items":
            page = arguments.get("page", 1)
            per_page = arguments.get("per_page", 10)
            data = await client.list_items(page, per_page)
        elif name == "get-item":
            item_id = arguments.get("id")
            if not item_id:
                return [
                    mcptypes.TextContent(type="text", text="Error: Missing item ID")
                ]
            data = await client.get_item(item_id)
        elif name == "create-item":
            data = await client.create_item(arguments)
        elif name == "upload-media":
            item_id = arguments.get("item_id")
            file_path = arguments.get("file_path")
            media_url = arguments.get("media_url")
            title = arguments.get("dcterms:title")

            if not item_id:
                return [
                    mcptypes.TextContent(type="text", text="Error: Missing item_id")
                ]
            if not file_path and not media_url:
                return [
                    mcptypes.TextContent(
                        type="text",
                        text="Error: Either file_path or media_url must be provided",
                    )
                ]
            if file_path:
                data = await client.upload_media_from_file(item_id, file_path, title)
            else:
                data = await client.upload_media_from_url(item_id, media_url, title)
        else:
            return [mcptypes.TextContent(type="text", text=f"Unknown tool {name}")]
        return [mcptypes.TextContent(type="text", text=str(data))]
    except Exception as e:
        return [mcptypes.TextContent(type="text", text=f"Error: {e!s}")]


async def main():
    print("Launching Omeka S MCP server...")

    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="OmekaSMCP",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
