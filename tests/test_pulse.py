import unittest, json
from unittest.mock import patch, MagicMock

from main import Optimizer


class TestOptimizerPulse(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_fetch_rpc(self, mock_urlopen):
        mock_res = MagicMock()
        mock_res.read.side_effect = [
            json.dumps({"result": "ok"}).encode(),
            json.dumps({"result": 12345678}).encode(),
            json.dumps({"result": {"value": {"blockhash": "FakeHash123"}}}).encode(),
        ]
        mock_urlopen.return_value = mock_res

        opt = Optimizer()
        snap = opt.fetch_rpc()

        self.assertEqual(snap["health"], "ok")
        self.assertEqual(snap["slot"], 12345678)
        self.assertEqual(snap["blockhash"], "FakeHash123")
        self.assertIn("timestamp", snap)


if __name__ == "__main__":
    unittest.main()
