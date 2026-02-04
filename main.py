import sys, json, os, time, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

RPC_URL = "https://api.devnet.solana.com"
DATA_DIR = "data"
SNAPSHOT_FILE = os.path.join(DATA_DIR, "snapshots.jsonl")
STRATEGY_FILE = "config/strategy.json"

class Optimizer:
    def fetch_rpc(self):
        def call(method):
            req = urllib.request.Request(RPC_URL, data=json.dumps({"jsonrpc":"2.0","id":1,"method":method}).encode(), headers={'Content-Type':'application/json'})
            return json.loads(urllib.request.urlopen(req).read())['result']
        return {"timestamp": time.time(), "health": call("getHealth"), "slot": call("getSlot"), "blockhash": call("getLatestBlockhash")['value']['blockhash']}

    def once(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        snap = self.fetch_rpc()
        with open(SNAPSHOT_FILE, "a") as f: f.write(json.dumps(snap) + "\n")
        print(f"Snapshot saved: Slot {snap['slot']}")

    def plan(self):
        with open(STRATEGY_FILE) as f: strat = json.load(f)
        snaps = []
        if os.path.exists(SNAPSHOT_FILE):
            with open(SNAPSHOT_FILE) as f: snaps = [json.loads(l) for l in f]
        latest = snaps[-1] if snaps else {"slot": 0}
        plan = {"target": strat['target'], "allocation": "Kamino: 60%, Jupiter: 40%", "risk_flags": ["Devnet-Only"], "ref_slot": latest['slot']}
        print(json.dumps(plan, indent=2))
        return plan

class Dashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Solana Yield Agent</h1><p>Check console for latest plan.</p></body></html>")

def serve():
    print("Serving at http://localhost:8000")
    HTTPServer(('localhost', 8000), Dashboard).serve_forever()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    opt = Optimizer()
    if cmd == "once": opt.once()
    elif cmd == "plan": opt.plan()
    elif cmd == "serve": serve()
    else: print("Usage: main.py once|plan|serve")