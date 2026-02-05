from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any


def get_json(url: str, *, timeout_s: int = 10, retries: int = 2) -> Any:
    """
    Fetch JSON using only the Python standard library.

    This is intentionally small and robust for low-resource machines:
    - short timeouts
    - small retry budget
    """

    headers = {"User-Agent": "solana-yield-optimizer/0.1", "Accept": "application/json"}
    last_err: str | None = None
    for attempt in range(max(0, int(retries)) + 1):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=int(timeout_s)) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body) if body else {}
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
            last_err = str(exc)
            time.sleep(min(2**attempt, 4))
    raise RuntimeError(f"GET JSON failed: {url} ({last_err})")


def apy_to_percent(value: Any) -> float:
    """
    Normalize APY numbers into *percent*.

    APIs vary:
    - Kamino often returns strings like "0.12" meaning 12% (fractional)
    - Meteora sometimes returns 5 meaning 5% (already percent)
    """

    try:
        x = float(value)
    except Exception:
        return 0.0
    if x <= 1.5:
        return x * 100.0
    return x

