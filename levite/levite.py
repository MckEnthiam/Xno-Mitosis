import json
import os
from datetime import datetime

RESPONSES_DIR = "../elijah/responses"
IDENTITY_FILE = "identity_state.json"

class Levite:
    def __init__(self):
        self.state = self.load_identity()

    def load_identity(self):
        if not os.path.exists(IDENTITY_FILE):
            return {
                "version": 1,
                "identity": {},
                "history": []
            }
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_identity(self):
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def process_session(self, session_path):
        for file in sorted(os.listdir(session_path)):
            if file.endswith(".json"):
                self.process_response(os.path.join(session_path, file))
        self.save_identity()

    def process_response(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        answer = data["answer"].strip()
        question_id = data["question_id"]

        extracted = self.extract_state(answer)

        if extracted:
            self.update_identity(extracted, question_id)

    def extract_state(self, answer):
        # BASE MINIMALE : extensible plus tard
        lowered = answer.lower()

        if lowered.startswith("je suis"):
            return {
                "type": "affirmation",
                "key": "self_statement",
                "value": answer
            }

        if "je pense" in lowered or "peut-être" in lowered:
            return {
                "type": "doute",
                "key": "self_statement",
                "value": answer
            }

        return None

    def update_identity(self, extracted, question_id):
        key = extracted["key"]
        value = extracted["value"]

        previous = self.state["identity"].get(key)

        event = {
            "timestamp": datetime.now().isoformat(),
            "question_id": question_id,
            "type": extracted["type"],
            "value": value,
            "previous": previous
        }

        if previous and previous != value:
            event["contradiction"] = True
        else:
            event["contradiction"] = False

        self.state["identity"][key] = value
        self.state["history"].append(event)
        self.state["version"] += 1

if __name__ == "__main__":
    levite = Levite()
    session_id = input("Session ID Elijah : ")
    session_path = os.path.join(RESPONSES_DIR, session_id)

    if os.path.exists(session_path):
        levite.process_session(session_path)
        print("Levite : identité mise à jour.")
    else:
        print("Session introuvable.")
