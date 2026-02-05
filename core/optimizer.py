class YieldOptimizer:
    def __init__(self, adapters):
        self.adapters = adapters
        self.market_data = []

    def sync_market_data(self):
        self.market_data = []
        for adapter in self.adapters:
            self.market_data.append(adapter.get_yield_data())

    def plan_strategy(self, investment_amount: float):
        """Deterministic planning: Allocates to the highest APY first."""
        if not self.market_data:
            self.sync_market_data()

        # Sort by APY descending
        sorted_pools = sorted(self.market_data, key=lambda x: x['apy'], reverse=True)
        
        # Simple deterministic split: 70% to best, 30% to second best for risk mitigation
        allocations = []
        if len(sorted_pools) >= 2:
            allocations.append({"protocol": sorted_pools[0]['name'], "amount": investment_amount * 0.7, "apy": sorted_pools[0]['apy']})
            allocations.append({"protocol": sorted_pools[1]['name'], "amount": investment_amount * 0.3, "apy": sorted_pools[1]['apy']})
        elif sorted_pools:
            allocations.append({"protocol": sorted_pools[0]['name'], "amount": investment_amount, "apy": sorted_pools[0]['apy']})

        projected_return = sum((a['amount'] * (a['apy'] / 100)) for a in allocations)
        
        return {
            "total_value": investment_amount,
            "allocations": allocations,
            "projected_return": projected_return
        }