import hashlib
import json
from datetime import datetime

class YieldOptimizer:
    """
    Core logic for yield optimization with verifiable reasoning.
    """
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.history = []

    def generate_plan(self, vault_data):
        """
        Generates a deterministic plan based on input data.
        Implements privacy by hashing sensitive vault identifiers.
        """
        # Privacy: Hash the vault address to prevent leaking sensitive on-chain IDs in logs
        vault_id = vault_data.get("address", "unknown")
        private_id = hashlib.sha256(vault_id.encode()).hexdigest()[:16]

        apy = vault_data.get("apy", 0)
        tvl = vault_data.get("tvl", 0)

        # Deterministic reasoning
        action = "HOLD"
        if apy > 0.15 and tvl > 1000000:
            action = "ALLOCATE"
        elif apy < 0.02:
            action = "WITHDRAW"

        plan = {
            "timestamp": datetime.utcnow().isoformat(),
            "vault_hash": private_id,
            "decision": action,
            "reasoning": f"APY {apy} meets threshold for {action}"
        }

        # Verifiable reasoning: Create a commitment hash of the plan
        plan_json = json.dumps(plan, sort_keys=True)
        plan["commitment"] = hashlib.sha256(plan_json.encode()).hexdigest()
        
        return plan
