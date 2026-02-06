class YieldOptimizer:
    def __init__(self, privacy_provider=None):
        self.privacy_provider = privacy_provider

    def generate_plan(self, opportunities):
        # Deterministic selection of highest APY
        best = max(opportunities, key=lambda x: x['apy'])
        
        plan = {
            "protocol": best['protocol'],
            "apy": best['apy'],
            "action": "DEPOSIT"
        }

        if self.privacy_provider:
            # Apply privacy increment: generate stealth address for the transaction
            plan['stealth_address'] = self.privacy_provider.generate_stealth_destination()
            
        return plan