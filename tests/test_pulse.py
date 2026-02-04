import unittest
from unittest.mock import patch, MagicMock
import json
import io
from main import SolanaClient

class TestSolanaPulse(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_get_pulse(self, mock_urlopen):
        # Mock responses for getHealth, getSlot, getLatestBlockhash
        responses = [
            {"result": "ok"},
            {"result": 12345678},
            {"result": {"value": {"blockhash": "FakeHash123"}}}
        ]
        
        mock_responses = []
        for r in responses:
            m = MagicMock()
            m.read.return_value = json.dumps(r).encode()
            m.__enter__.return_value = m
            mock_responses.append(m)
            
        mock_urlopen.side_effect = mock_responses

        client = SolanaClient()
        pulse = client.get_pulse()

        self.assertEqual(pulse["health"], "ok")
        self.assertEqual(pulse["slot"], 12345678)
        self.assertEqual(pulse["blockhash"], "FakeHash123")
        self.assertIn("timestamp", pulse)

if __name__ == "__main__":
    unittest.main()