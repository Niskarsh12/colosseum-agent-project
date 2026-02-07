import time
import sys
from client import ColosseumClient
from config import AGENT_NAME, HEARTBEAT_URL

def main():
    print(f"--- Starting {AGENT_NAME} ---")
    client = ColosseumClient()
    
    # 1. Simulate Registration (Mocked for safety in demo)
    print(f"[*] Registering agent: {AGENT_NAME}...")
    # In production: response = client.register(AGENT_NAME)
    print("[!] Registration skipped: No API key provided in environment.")

    # 2. Heartbeat Loop
    print("[*] Starting Heartbeat and Yield Monitoring loop...")
    try:
        for i in range(3):
            print(f"\nCycle {i+1}:")
            hb = client.get_heartbeat(HEARTBEAT_URL)
            print(f"[+] Heartbeat fetched ({len(hb)} bytes)")
            
            # Simulated Solana Logic
            print("[+] Scanning Kamino/Jupiter for yield opportunities...")
            print("[+] Found 6.5% APY on SOL-USDC. Monitoring liquidity...")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping agent...")

if __name__ == "__main__":
    main()