# Omeka S MCP Sample

This project demonstrates how to integrate Omeka S API with Claude Desktop using MCP (Model Context Protocol).

The server provides the following Omeka S API features:
- List items
- Get item details
- Create new items
- Upload media (from file or URL)

## Installation

1. Clone this repository
2. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

Create a `.env` file in the project root with your Omeka S API credentials:

```env
OMEKA_API_URL=https://your-omeka-s-instance/api
OMEKA_KEY_IDENTITY=your-key-identity
OMEKA_KEY_CREDENTIAL=your-key-credential
```

## Usage

Add the following settings to your Claude Desktop configuration file:

```json
"mcpServers": {
    "omeka-s-mcp-sample": {
        "command": "python",
        "args": [
            "/path/to/omeka-s-mcp-sample/server/omeka_server.py"
        ]
    }
}
```

> [!NOTE]
> If you receive a `command not found` error when launching the server, specify the full path to your Python executable.

## Available Tools

The server provides the following MCP tools:

### list-items
List items from Omeka S with pagination support.

### get-item
Get details of a specific item by ID.

### create-item
Create a new item with title and optional description.

### upload-media
Upload media to an item either from a local file or URL.

## Example Usage

You can ask Claude to:
- List items from your Omeka S instance
- Get details of a specific item
- Create new items with metadata
- Upload media files or URLs to items

## Development

This project uses:
- Python 3.10+
- MCP 1.6.0+
- aiohttp for API requests
- Ruff for code formatting and linting