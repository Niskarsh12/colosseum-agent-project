import sys

from core.optimizer import YieldOptimizer
from adapters.mock_protocols import KaminoAdapter as MockKaminoAdapter, MeteoraAdapter as MockMeteoraAdapter
from adapters.kamino import KaminoAdapter
from adapters.meteora import MeteoraAdapter

def main():
    print("--- Solana Yield Optimizer Prototype ---")
    
    # Default token mint for Meteora vault APY (USDC mint).
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

    # Initialize real adapters (read-only). If a network call fails at runtime,
    # YieldOptimizer will fall back to mock values.
    adapters = [KaminoAdapter(max_vaults=3), MeteoraAdapter(token_mint=usdc_mint)]
    
    optimizer = YieldOptimizer(adapters, fallback_adapters=[MockKaminoAdapter(), MockMeteoraAdapter()])
    
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
