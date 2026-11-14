"""Minimal client for the AnkiConnect add-on (API version 6)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "http://127.0.0.1:8765"


class AnkiConnectError(RuntimeError):
    pass


class AnkiConnect:
    def __init__(self, url: str = DEFAULT_URL, timeout: float = 30.0) -> None:
        self.url = url
        self.timeout = timeout

    def invoke(self, action: str, **params: Any) -> Any:
        payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
        req = urllib.request.Request(self.url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.load(resp)
        except urllib.error.URLError as e:
            raise AnkiConnectError(
                f"Could not reach AnkiConnect at {self.url}. Is Anki open with AnkiConnect installed? ({e.reason})"
            ) from e
        if body.get("error") is not None:
            raise AnkiConnectError(f"{action}: {body['error']}")
        return body["result"]
