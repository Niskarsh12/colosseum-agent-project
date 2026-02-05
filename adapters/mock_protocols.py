from __future__ import annotations

from .protocols import ProtocolAdapter

class KaminoAdapter(ProtocolAdapter):
    def get_yield_data(self):
        # Mocking API response
        return {"name": "Kamino", "apy": 8.5, "tvl": 500_000_000}

class MeteoraAdapter(ProtocolAdapter):
    def get_yield_data(self):
        # Mocking API response
        return {"name": "Meteora", "apy": 12.2, "tvl": 150_000_000}
