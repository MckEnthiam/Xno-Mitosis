import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDENTITY_FILE = os.path.join(BASE_DIR, "identity_state.json")


class Levite:
    def __init__(self):
        self.state = self._load()

    def _load(self):
        if not os.path.exists(IDENTITY_FILE):
            return {"version": 1, "identity": {}, "history": []}
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def process(self, answer):
        event = {
            "timestamp": datetime.now().isoformat(),
            "value": answer
        }
        self.state["history"].append(event)
        self.state["version"] += 1
        self._save()

    def _save(self):
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
