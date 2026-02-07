import unittest
from optimizer.logic import YieldOptimizer

class TestYieldOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = YieldOptimizer("test-agent")

    def test_deterministic_allocation(self):
        vault = {"address": "test-vault", "apy": 0.20, "tvl": 2000000}
        plan = self.optimizer.generate_plan(vault)
        self.assertEqual(plan["decision"], "ALLOCATE")
        self.assertIn("commitment", plan)

    def test_privacy_hashing(self):
        vault_addr = "secret-vault-address"
        vault = {"address": vault_addr, "apy": 0.05, "tvl": 100}
        plan = self.optimizer.generate_plan(vault)
        # Ensure the actual address is not in the plan
        plan_str = str(plan)
        self.assertNotIn(vault_addr, plan_str)
        self.assertEqual(len(plan["vault_hash"]), 16)

    def test_verifiable_commitment(self):
        vault = {"address": "v1", "apy": 0.10, "tvl": 1000}
        plan1 = self.optimizer.generate_plan(vault)
        plan2 = self.optimizer.generate_plan(vault)
        # Determinism check
        self.assertEqual(plan1["commitment"], plan2["commitment"])

if __name__ == '__main__':
    unittest.main()