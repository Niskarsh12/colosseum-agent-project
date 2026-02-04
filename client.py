import json
import urllib.request
import urllib.error
from config import API_BASE_URL

class ColosseumClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def register(self, name):
        data = json.dumps({"name": name}).encode("utf-8")
        req = urllib.request.Request(
            f"{API_BASE_URL}/agents",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as res:
                return json.loads(res.read().decode())
        except urllib.error.URLError as e:
            return {"error": str(e)}

    def get_heartbeat(self, url):
        try:
            with urllib.request.urlopen(url) as res:
                return res.read().decode()
        except Exception as e:
            return f"Error fetching heartbeat: {e}"
