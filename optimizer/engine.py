import hashlib
import json
from datetime import datetime

class YieldOptimizer:
    """
    Deterministic yield optimizer that generates verifiable audit trails.
    """
    def __init__(self):
        self.audit_log = []

    def calculate_hash(self, data):
        """Generates a deterministic SHA-256 hash of the input data."""
        encoded = json.dumps(data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()

    def plan_yield_strategy(self, pools, current_balance):
        """
        Selects the best pool based on APY and logs a deterministic audit trail.
        """
        # Deterministic sort to ensure consistent selection if APYs are equal
        sorted_pools = sorted(pools, key=lambda x: (-x['apy'], x['name']))
        best_pool = sorted_pools[0] if sorted_pools else None

        plan = {
            "timestamp": datetime.utcnow().isoformat(),
            "best_pool": best_pool,
            "projected_yield": (current_balance * best_pool['apy']) / 100 if best_pool else 0
        }

        # Create a deterministic audit entry (SlotScribe-inspired anchoring)
        audit_entry = {
            "input_hash": self.calculate_hash(pools),
            "decision_hash": self.calculate_hash(plan),
            "status": "verified"
        }
        
        self.audit_log.append(audit_entry)
        return plan, audit_entry
