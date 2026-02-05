import unittest
from api_client import ColosseumClient

class TestHackathonLogic(unittest.TestCase):
    def test_client_init(self):
        client = ColosseumClient(api_key="test_key")
        self.assertEqual(client.api_key, "test_key")

    def test_base_url(self):
        self.assertEqual(ColosseumClient.BASE_URL, "https://agents.colosseum.com/api")

if __name__ == '__main__':
    unittest.main()