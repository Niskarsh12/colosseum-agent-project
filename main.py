import sys
from core.optimizer import YieldOptimizer
from adapters.mock_protocols import KaminoAdapter, MeteoraAdapter

def main():
    print("--- Solana Yield Optimizer Prototype ---")
    
    # Initialize adapters
    adapters = [
        KaminoAdapter(),
        MeteoraAdapter()
    ]
    
    optimizer = YieldOptimizer(adapters)
    
    print("Fetching current yields...")
    optimizer.sync_market_data()
    
    print("\nGenerating deterministic strategy...")
    strategy = optimizer.plan_strategy(investment_amount=1000.0)
    
    print(f"\nRecommended Allocation (Total: ${strategy['total_value']}):")
    for allocation in strategy['allocations']:
        print(f"- {allocation['protocol']}: ${allocation['amount']:.2f} @ {allocation['apy']}% APY")
    
    print(f"\nProjected Annual Return: ${strategy['projected_return']:.2f}")

if __name__ == '__main__':
    main()