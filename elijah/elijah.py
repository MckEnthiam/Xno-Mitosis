import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "elijah_questions.json")
RESPONSES_DIR = os.path.join(BASE_DIR, "responses")

class Elijah:
    def __init__(self, questions_file):
        self.questions_file = questions_file
        self.questions = self.load_questions()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.responses_path = os.path.join(RESPONSES_DIR, self.session_id)
        os.makedirs(self.responses_path, exist_ok=True)

    def load_questions(self):
        with open(self.questions_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def ask_questions(self):
        for q_id in sorted(self.questions.keys()):
            question = self.questions[q_id]
            print(f"[{q_id}] {question}")
            answer = input("> ")

            self.save_response(q_id, question, answer)

    def save_response(self, q_id, question, answer):
        data = {
            "question_id": q_id,
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }

        file_path = os.path.join(self.responses_path, f"{q_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    elijah = Elijah(QUESTIONS_FILE)
    elijah.ask_questions()
