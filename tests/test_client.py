import unittest
from client import ColosseumClient

class TestColosseumClient(unittest.TestCase):
    def setUp(self):
        self.client = ColosseumClient()

    def test_client_init(self):
        self.assertEqual(self.client.api_key, None)

    def test_heartbeat_fetch_fail(self):
        # Test with invalid URL to ensure error handling works
        result = self.client.get_heartbeat("http://invalid.url.local")
        self.assertIn("Error", result)

if __name__ == '__main__':
    unittest.main()