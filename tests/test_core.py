import unittest, json, os
from unittest.mock import patch, MagicMock
from main import Optimizer

class TestOptimizer(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_rpc_polling(self, mock_url):
        mock_res = MagicMock()
        mock_res.read.side_effect = [
            json.dumps({"result": "ok"}).encode(),
            json.dumps({"result": 12345}).encode(),
            json.dumps({"result": {"value": {"blockhash": "abc"}}}).encode()
        ]
        mock_url.return_value = mock_res
        
        opt = Optimizer()
        snap = opt.fetch_rpc()
        self.assertEqual(snap['slot'], 12345)
        self.assertEqual(snap['blockhash'], "abc")

    def test_plan_generation(self):
        if not os.path.exists('config'): os.makedirs('config')
        with open('config/strategy.json', 'w') as f:
            json.dump({"target": "test"}, f)
        
        opt = Optimizer()
        plan = opt.plan()
        self.assertEqual(plan['target'], "test")
        self.assertIn("allocation", plan)