import sys
from core.optimizer import YieldOptimizer
from adapters.privacy_provider import SipherAdapter

def main():
    print("--- Solana Yield Optimizer v1.5.2 ---")
    
    # Initialize privacy layer based on forum feedback
    privacy_layer = SipherAdapter(api_base="https://api.sipher.xyz")
    optimizer = YieldOptimizer(privacy_provider=privacy_layer)
    
    print("[1] Scanning Solana protocols for yield...")
    opportunities = [
        {"protocol": "Kamino", "apy": 0.12, "vault": "USDC-SOL"},
        {"protocol": "Meteora", "apy": 0.15, "vault": "USDC-SOL"}
    ]
    
    print("[2] Calculating optimal path...")
    plan = optimizer.generate_plan(opportunities)
    
    print(f"[3] Execution Plan: {plan['action']} on {plan['protocol']} at {plan['apy']*100}%")
    
    if plan.get('stealth_address'):
        print(f"[4] Privacy Shield Active: Routing via {plan['stealth_address']}")

if __name__ == '__main__':
    main()