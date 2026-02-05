import unittest

from adapters.mock_protocols import KaminoAdapter, MeteoraAdapter


class TestMockAdapters(unittest.TestCase):
    def test_kamino_shape(self):
        data = KaminoAdapter().get_yield_data()
        self.assertIn("name", data)
        self.assertIn("apy", data)
        self.assertIn("tvl", data)
        self.assertEqual(data["name"], "Kamino")

    def test_meteora_shape(self):
        data = MeteoraAdapter().get_yield_data()
        self.assertIn("name", data)
        self.assertIn("apy", data)
        self.assertIn("tvl", data)
        self.assertEqual(data["name"], "Meteora")


if __name__ == "__main__":
    unittest.main()

