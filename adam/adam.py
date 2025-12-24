import json
import time

IDENTITY_FILE = "../levite/identity_state.json"

class Adam:
    def __init__(self, identity_file):
        self.identity_file = identity_file
        self.identity = self.load_identity()

    def load_identity(self):
        try:
            with open(self.identity_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("identity", {})
        except FileNotFoundError:
            return {}

    def respond(self, question):
        q = question.lower()

        if "qui es-tu" in q or "qui es tu" in q:
            return self.compose_identity()

        if "nom" in q:
            return self.identity.get("name", "je ne sais pas")

        if "âge" in q or "age" in q:
            return self.identity.get("age", "je ne sais pas")

        if "penses-tu" in q or "crois-tu" in q:
            return "je ne sais pas"

        return "je ne sais pas, ne sais plus, peut etre saurais plus tard?";

    def compose_identity(self):
        name = self.identity.get("name")
        age = self.identity.get("age")

        if name and age:
            return f"je suis {name} et j’ai {age}"
        if name:
            return f"je suis {name}"
        if age:
            return f"j’ai {age}"
        return "je ne sais pas"

if __name__ == "__main__":
    adam = Adam(IDENTITY_FILE)
    print("Adam est actif. Pose une question.")
    print("Tape 'exit' pour quitter.\n")

    while True:
        question = input("Yehi>> ")
        if question.lower() == "exit":
            break
        response = adam.respond(question)
        print(response)
