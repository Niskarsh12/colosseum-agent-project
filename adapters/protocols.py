from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypedDict


class YieldData(TypedDict, total=False):
    """
    Common yield data schema used by the optimizer.

    - name: human readable identifier (protocol/strategy)
    - apy: APY in *percent* (e.g., 8.5 means 8.5% APY)
    - tvl: approximate TVL in USD (optional)
    - source: where the data came from (optional)
    """

    name: str
    apy: float
    tvl: float
    source: str


class ProtocolAdapter(Protocol):
    def get_yield_data(self) -> YieldData: ...


@dataclass(frozen=True)
class AdapterError(RuntimeError):
    message: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message

