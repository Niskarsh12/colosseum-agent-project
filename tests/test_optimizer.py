import unittest
from core.optimizer import YieldOptimizer
from adapters.privacy_provider import SipherAdapter

class TestYieldOptimizer(unittest.TestCase):
    def setUp(self):
        self.opps = [
            {"protocol": "A", "apy": 0.05},
            {"protocol": "B", "apy": 0.10}
        ]

    def test_deterministic_selection(self):
        optimizer = YieldOptimizer()
        plan = optimizer.generate_plan(self.opps)
        self.assertEqual(plan['protocol'], "B")
        self.assertEqual(plan['apy'], 0.10)

    def test_privacy_integration(self):
        adapter = SipherAdapter("http://mock")
        optimizer = YieldOptimizer(privacy_provider=adapter)
        plan = optimizer.generate_plan(self.opps)
        self.assertIn('stealth_address', plan)
        self.assertTrue(plan['stealth_address'].startswith('v1_stealth_'))

if __name__ == '__main__':
    unittest.main()