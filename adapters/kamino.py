from __future__ import annotations

from typing import Any

from .http_json import apy_to_percent, get_json
from .protocols import ProtocolAdapter, YieldData


class KaminoAdapter(ProtocolAdapter):
    """
    Read-only adapter for Kamino Earn vault yields.

    Uses Kamino public API:
    - List vaults: GET https://api.kamino.finance/kvaults/vaults
    - Metrics:     GET https://api.kamino.finance/kvaults/{vaultPubkey}/metrics
    """

    BASE_URL = "https://api.kamino.finance"

    def __init__(self, *, max_vaults: int = 3, timeout_s: int = 10):
        self.max_vaults = max(1, min(int(max_vaults), 10))
        self.timeout_s = int(timeout_s)

    def get_yield_data(self) -> YieldData:
        vaults = get_json(f"{self.BASE_URL}/kvaults/vaults", timeout_s=self.timeout_s, retries=2)
        if not isinstance(vaults, list) or not vaults:
            raise RuntimeError("Kamino vault list empty/unexpected")

        best: dict[str, Any] | None = None
        best_apy = -1.0
        best_tvl = 0.0
        best_name = "Kamino"

        for v in vaults[: self.max_vaults]:
            if not isinstance(v, dict):
                continue
            pubkey = v.get("vaultPubkey") or v.get("pubkey")
            state = v.get("state", {}) if isinstance(v.get("state"), dict) else {}
            name = state.get("name") if isinstance(state.get("name"), str) else None
            if not isinstance(pubkey, str) or not pubkey.strip():
                continue

            metrics = get_json(f"{self.BASE_URL}/kvaults/{pubkey}/metrics", timeout_s=self.timeout_s, retries=2)
            if not isinstance(metrics, dict):
                continue

            apy_raw = metrics.get("apy7d") or metrics.get("apy30d") or metrics.get("apy") or 0.0
            apy = apy_to_percent(apy_raw)

            tvl = 0.0
            for k in ("tokensAvailableUsd", "tokensInvestedUsd"):
                try:
                    tvl += float(metrics.get(k) or 0.0)
                except Exception:
                    pass

            if apy > best_apy:
                best_apy = apy
                best_tvl = tvl
                best = metrics
                if name:
                    best_name = f"Kamino Earn: {name}"

        if best is None or best_apy <= 0.0:
            raise RuntimeError("Kamino metrics unavailable")

        return {"name": best_name, "apy": float(best_apy), "tvl": float(best_tvl), "source": "kamino"}
