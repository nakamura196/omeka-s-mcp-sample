import mcp.types as mcptypes


def get_tools() -> list[mcptypes.Tool]:
    """利用可能なツールの一覧を返す"""
    return [
        mcptypes.Tool(
            name="list-items",
            description="List items from Omeka S.",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number",
                    },
                    "per_page": {
                        "type": "integer",
                        "description": "Items per page",
                    },
                },
                "required": [],
            },
        ),
        mcptypes.Tool(
            name="get-item",
            description="Get a specific item from Omeka S.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Item ID",
                    },
                },
                "required": ["id"],
            },
        ),
        mcptypes.Tool(
            name="create-item",
            description="Create a new item in Omeka S.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dcterms:title": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "@value": {
                                    "type": "string",
                                    "description": "Title of the item",
                                },
                                "@type": {
                                    "type": "string",
                                    "description": (
                                        "Type of the value (e.g., 'literal')"
                                    ),
                                },
                            },
                            "required": ["@value"],
                        },
                    },
                    "dcterms:description": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "@value": {
                                    "type": "string",
                                    "description": "Description of the item",
                                },
                                "@type": {
                                    "type": "string",
                                    "description": (
                                        "Type of the value (e.g., 'literal')"
                                    ),
                                },
                            },
                            "required": ["@value"],
                        },
                    },
                },
                "required": ["dcterms:title"],
            },
        ),
        mcptypes.Tool(
            name="upload-media",
            description="Upload media to an item in Omeka S.",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "integer",
                        "description": "ID of the item to attach media to",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to upload",
                    },
                    "media_url": {
                        "type": "string",
                        "description": "URL of the media to upload",
                    },
                    "dcterms:title": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "@value": {
                                    "type": "string",
                                    "description": "Title of the media",
                                },
                                "@type": {
                                    "type": "string",
                                    "description": (
                                        "Type of the value (e.g., 'literal')"
                                    ),
                                },
                            },
                            "required": ["@value"],
                        },
                    },
                },
                "required": ["item_id"],
                "oneOf": [
                    {"required": ["file_path"]},
                    {"required": ["media_url"]},
                ],
            },
        ),
    ]
