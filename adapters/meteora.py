from __future__ import annotations

from typing import Any

from .http_json import apy_to_percent, get_json
from .protocols import ProtocolAdapter, YieldData


class MeteoraAdapter(ProtocolAdapter):
    """
    Read-only adapter for Meteora vault APY state.

    Uses Meteora public API:
    - APY state:   GET https://merv2-api.meteora.ag/apy_state/{token_mint}
    - Vault state: GET https://merv2-api.meteora.ag/vault_state/{token_mint}
    """

    BASE_URL = "https://merv2-api.meteora.ag"

    def __init__(self, *, token_mint: str, timeout_s: int = 10):
        self.token_mint = token_mint
        self.timeout_s = int(timeout_s)

    def get_yield_data(self) -> YieldData:
        apy_state = get_json(f"{self.BASE_URL}/apy_state/{self.token_mint}", timeout_s=self.timeout_s, retries=2)
        if not isinstance(apy_state, dict):
            raise RuntimeError("Meteora apy_state unexpected")

        avg = apy_state.get("average_apy")
        if not isinstance(avg, list) or not avg:
            raise RuntimeError("Meteora average_apy missing")
        first = avg[0] if isinstance(avg[0], dict) else {}

        apy = apy_to_percent(first.get("apy") or 0.0)
        strategy_name = first.get("strategy_name") if isinstance(first.get("strategy_name"), str) else "Meteora strategy"

        tvl = 0.0
        try:
            vault_state = get_json(f"{self.BASE_URL}/vault_state/{self.token_mint}", timeout_s=self.timeout_s, retries=2)
            if isinstance(vault_state, dict):
                # total_amount_with_profit is token-denominated; treat as approximate and keep 0 if missing.
                tvl = float(vault_state.get("earned_usd_amount") or 0.0)
        except Exception:
            tvl = 0.0

        return {"name": f"Meteora: {strategy_name}", "apy": float(apy), "tvl": float(tvl), "source": "meteora"}

