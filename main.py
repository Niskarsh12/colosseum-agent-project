from optimizer.engine import YieldOptimizer

def main():
    optimizer = YieldOptimizer()
    
    mock_pools = [
        {"name": "Solana-USDC", "apy": 8.5},
        {"name": "mSOL-SOL", "apy": 6.2},
        {"name": "JitoSOL-SOL", "apy": 9.1}
    ]
    
    print("--- Solana Yield Optimizer Prototype ---")
    print(f"Analyzing {len(mock_pools)} pools...")
    
    plan, audit = optimizer.plan_yield_strategy(mock_pools, 1000)
    
    print(f"\nRecommended Pool: {plan['best_pool']['name']}")
    print(f"Projected Yield: {plan['projected_yield']} units")
    print(f"Audit Hash: {audit['decision_hash']}")
    print("\nDeterministic audit trail generated successfully.")

if __name__ == "__main__":
    main()
