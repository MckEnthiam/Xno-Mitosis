import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDENTITY_FILE = os.path.join(BASE_DIR, "identity_state.json")


class Levite:
    """
    LEVITE
    - Ne comprend pas
    - Ne corrige pas
    - Ne juge pas
    - Transforme des réponses brutes en états persistants
    """

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        if not os.path.exists(IDENTITY_FILE):
            return {
                "version": 0,
                "identity": {},
                "history": []
            }

        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_state(self):
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def process_session(self, session_path):
        """
        Traite une session Elijah complète
        """
        if not os.path.exists(session_path):
            return

        files = sorted(
            f for f in os.listdir(session_path)
            if f.endswith(".json")
        )

        for filename in files:
            file_path = os.path.join(session_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._process_response(data)

        self.state["version"] += 1
        self._save_state()

    def _process_response(self, data):
        """
        Enregistre une réponse sans interprétation
        """
        q_id = data.get("question_id")
        question = data.get("question")
        answer = data.get("answer")

        event = {
            "timestamp": datetime.now().isoformat(),
            "question_id": q_id,
            "question": question,
            "value": answer
        }

        # Historique brut
        self.state["history"].append(event)

        # État d'identité brut
        self.state["identity"][f"q_{q_id}"] = answer
