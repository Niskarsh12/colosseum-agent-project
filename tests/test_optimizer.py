import unittest
from optimizer.engine import YieldOptimizer

class TestYieldOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = YieldOptimizer()
        self.pools = [
            {"name": "Pool A", "apy": 10.0},
            {"name": "Pool B", "apy": 15.0}
        ]

    def test_deterministic_selection(self):
        plan1, audit1 = self.optimizer.plan_yield_strategy(self.pools, 100)
        plan2, audit2 = self.optimizer.plan_yield_strategy(self.pools, 100)
        
        self.assertEqual(plan1['best_pool']['name'], "Pool B")
        self.assertEqual(audit1['decision_hash'], audit2['decision_hash'])

    def test_hash_consistency(self):
        data = {"test": 123}
        hash1 = self.optimizer.calculate_hash(data)
        hash2 = self.optimizer.calculate_hash(data)
        self.assertEqual(hash1, hash2)

if __name__ == '__main__':
    unittest.main()
