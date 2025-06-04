import os
from urllib.parse import urlencode

# Omeka Sの設定
OMEKA_API_URL = os.getenv("OMEKA_API_URL", "http://localhost:8080/api")
OMEKA_KEY_IDENTITY = os.getenv("OMEKA_KEY_IDENTITY", "")
OMEKA_KEY_CREDENTIAL = os.getenv("OMEKA_KEY_CREDENTIAL", "")


def get_auth_url(base_url: str) -> str:
    """認証パラメータを追加したURLを生成"""
    params = {
        "key_identity": OMEKA_KEY_IDENTITY,
        "key_credential": OMEKA_KEY_CREDENTIAL,
    }
    return f"{base_url}?{urlencode(params)}"
