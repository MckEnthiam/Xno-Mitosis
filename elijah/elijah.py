import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "elijah_questions.json")
RESPONSES_DIR = os.path.join(BASE_DIR, "responses")


class Elijah:
    def __init__(self):
        self.questions = self._load_questions()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_path = os.path.join(RESPONSES_DIR, self.session_id)
        os.makedirs(self.session_path, exist_ok=True)

    def _load_questions(self):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def ask(self):
        for q_id in sorted(self.questions.keys()):
            yield q_id, self.questions[q_id]

    def save_response(self, q_id, question, answer):
        data = {
            "question_id": q_id,
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }

        path = os.path.join(self.session_path, f"{q_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
