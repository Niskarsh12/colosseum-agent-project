import json
import unittest
from unittest.mock import MagicMock, patch

from adapters.kamino import KaminoAdapter
from adapters.meteora import MeteoraAdapter


def _mock_resp(payload):
    m = MagicMock()
    m.read.return_value = json.dumps(payload).encode("utf-8")
    m.__enter__.return_value = m
    return m


class TestLiveAdaptersParsing(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_kamino_parsing(self, mock_urlopen):
        # First call: vault list
        vaults = [
            {"vaultPubkey": "VaultPubkey1", "state": {"name": "USDC Vault"}},
        ]
        # Second call: metrics for that vault
        metrics = {"apy7d": "0.12", "tokensAvailableUsd": "100.0", "tokensInvestedUsd": "900.0"}

        mock_urlopen.side_effect = [_mock_resp(vaults), _mock_resp(metrics)]

        data = KaminoAdapter(max_vaults=1).get_yield_data()
        self.assertIn("Kamino", data["name"])
        self.assertAlmostEqual(data["apy"], 12.0, places=4)
        self.assertAlmostEqual(data["tvl"], 1000.0, places=4)

    @patch("urllib.request.urlopen")
    def test_meteora_parsing(self, mock_urlopen):
        apy_state = {"average_apy": [{"apy": 5, "strategy_name": "mock-strategy"}]}
        vault_state = {"earned_usd_amount": "42.0"}
        mock_urlopen.side_effect = [_mock_resp(apy_state), _mock_resp(vault_state)]

        data = MeteoraAdapter(token_mint="AnyMint").get_yield_data()
        self.assertIn("Meteora", data["name"])
        self.assertEqual(data["apy"], 5.0)
        self.assertEqual(data["tvl"], 42.0)


if __name__ == "__main__":
    unittest.main()

