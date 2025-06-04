import json
from pathlib import Path
from typing import Any

import aiohttp

from server.omeka.config import OMEKA_API_URL, get_auth_url

HTTP_OK = 200
HTTP_CREATED = 201

class OmekaClient:
    def __init__(self):
        self.base_url = OMEKA_API_URL

    async def list_items(self, page: int = 1, per_page: int = 10) -> dict[str, Any]:
        """アイテム一覧を取得"""
        url = get_auth_url(f"{self.base_url}/items")
        params = {
            "page": page,
            "per_page": per_page
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == HTTP_OK:
                    return await response.json()
                else:
                    raise Exception(f"Error: {response.status}")

    async def get_item(self, item_id: int) -> dict[str, Any]:
        """特定のアイテムを取得"""
        url = get_auth_url(f"{self.base_url}/items/{item_id}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == HTTP_OK:
                    return await response.json()
                else:
                    raise Exception(f"Error: {response.status}")

    async def create_item(self, item_data: dict[str, Any]) -> dict[str, Any]:
        """新しいアイテムを作成"""
        url = get_auth_url(f"{self.base_url}/items")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=item_data) as response:
                if response.status == HTTP_CREATED:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Error: {response.status} - {error_text}")

    async def upload_media_from_file(
        self, item_id: int, file_path: str, title: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """ファイルからメディアをアップロード"""
        url = get_auth_url(f"{self.base_url}/media")
        path = Path(file_path)

        file_data = {
            "o:item": {"o:id": item_id},
            "o:ingester": "upload",
            "file_index": "0",
            "o:source": path.name,
        }

        if title:
            file_data["dcterms:title"] = title

        data = aiohttp.FormData()
        data.add_field("data", json.dumps(file_data), content_type="application/json")

        try:
            with open(path, "rb") as f:
                data.add_field("file[0]", f, filename=path.name, content_type="image")
        except Exception as e:
            raise Exception(f"Error reading file: {e!s}") from e

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == HTTP_CREATED:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Error: {response.status} - {error_text}")

    async def upload_media_from_url(
        self, item_id: int, media_url: str, title: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """URLからメディアをアップロード"""
        url = get_auth_url(f"{self.base_url}/media")

        file_data = {
            "o:item": {"o:id": item_id},
            "o:ingester": "url",
            "ingest_url": media_url,
            "o:source": media_url,
        }

        if title:
            file_data["dcterms:title"] = title

        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=file_data, headers=headers) as response:
                if response.status == HTTP_CREATED:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Error: {response.status} - {error_text}")
