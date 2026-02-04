import sys
import json
import os
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

RPC_URL = "https://api.devnet.solana.com"
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "snapshots.json")

class SolanaClient:
    def _rpc_call(self, method, params=None):
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
        }).encode("utf-8")
        req = urllib.request.Request(RPC_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())["result"]

    def get_pulse(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "health": self._rpc_call("getHealth"),
            "slot": self._rpc_call("getSlot"),
            "blockhash": self._rpc_call("getLatestBlockhash")["value"]["blockhash"]
        }

def save_snapshot(snapshot):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass
    
    history.append(snapshot)
    with open(DATA_FILE, "w") as f:
        json.dump(history[-50:], f, indent=2)

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        history = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                history = json.load(f)
        
        rows = "".join([f"<tr><td>{s['timestamp']}</td><td>{s['health']}</td><td>{s['slot']}</td><td>{s['blockhash']}</td></tr>" for s in reversed(history)])
        
        html = f"""
        <html><head><title>Solana Pulse</title><style>body{{font-family:sans-serif;padding:20px;}} table{{width:100%;border-collapse:collapse;}} th,td{{border:1px solid #ccc;padding:8px;text-align:left;}} th{{background:#f4f4f4;}}</style></head>
        <body><h1>Solana Pulse Dashboard</h1><table><tr><th>Time</th><th>Health</th><th>Slot</th><th>Blockhash</th></tr>{rows}</table></body></html>
        """
        self.wfile.write(html.encode())

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "once"
    client = SolanaClient()

    if cmd == "once":
        print("Fetching Solana pulse...")
        pulse = client.get_pulse()
        save_snapshot(pulse)
        print(json.dumps(pulse, indent=2))
    elif cmd == "serve":
        port = 8000
        print(f"Serving dashboard at http://localhost:{port}")
        HTTPServer(("", port), DashboardHandler).serve_forever()
    else:
        print("Unknown command. Use 'once' or 'serve'.")

if __name__ == "__main__":
    main()