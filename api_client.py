import json
import urllib.request
import urllib.error

class ColosseumClient:
    BASE_URL = "https://agents.colosseum.com/api"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def register_agent(self, name):
        data = json.dumps({"name": name}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/agents",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def get_heartbeat(self):
        # Heartbeat is markdown, not JSON
        url = "https://colosseum.com/heartbeat.md"
        with urllib.request.urlopen(url) as response:
            return response.read().decode()