import json
from optimizer.logic import YieldOptimizer

def main():
    print("--- Solana Yield Optimizer Agent ---")
    optimizer = YieldOptimizer(agent_id="agent-001")

    # Simulated vault data
    vaults = [
        {"address": "SOL-USDC-LP-123", "apy": 0.18, "tvl": 2500000},
        {"address": "STAKE-SOL-456", "apy": 0.01, "tvl": 5000000}
    ]

    for vault in vaults:
        plan = optimizer.generate_plan(vault)
        print(f"\n[Plan Generated]")
        print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()