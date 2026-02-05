import unittest
from core.optimizer import YieldOptimizer

class MockAdapter:
    def __init__(self, name, apy):
        self.name = name
        self.apy = apy
    def get_yield_data(self):
        return {"name": self.name, "apy": self.apy}

class TestOptimizer(unittest.TestCase):
    def test_deterministic_allocation(self):
        adapters = [MockAdapter("Low", 5.0), MockAdapter("High", 10.0)]
        optimizer = YieldOptimizer(adapters)
        strategy = optimizer.plan_strategy(1000.0)
        
        # High APY should get 70% ($700)
        high_alloc = next(a for a in strategy['allocations'] if a['protocol'] == "High")
        self.assertEqual(high_alloc['amount'], 700.0)
        self.assertEqual(len(strategy['allocations']), 2)

    def test_empty_adapters(self):
        optimizer = YieldOptimizer([])
        strategy = optimizer.plan_strategy(1000.0)
        self.assertEqual(len(strategy['allocations']), 0)

if __name__ == '__main__':
    unittest.main()