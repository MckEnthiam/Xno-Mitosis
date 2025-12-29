import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDENTITY_FILE = os.path.join(BASE_DIR, "../levite/identity_state.json")


class Adam:
    def __init__(self):
        self.identity = self._load_identity()

    def _load_identity(self):
        if not os.path.exists(IDENTITY_FILE):
            return {}
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("identity", {})

    def respond(self, question: str) -> str:
        q = question.lower()

        if "qui es" in q:
            return self.identity.get("self_statement", "je ne sais pas")

        if "nom" in q:
            return self.identity.get("name", "je ne sais pas")

        if "âge" in q or "age" in q:
            return self.identity.get("age", "je ne sais pas")

        return "je ne sais pas"
