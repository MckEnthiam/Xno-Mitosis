import json
import os

IDENTITY_FILE = "../levite/identity_state.json"

class Adam:
    """
    ADAM MODULE
    - Rejoue l'identité construite par Levite
    - Ne synthétise rien
    - Reformule localement
    - Incohérent globalement
    - Ne conclut jamais
    """
    
    def __init__(self, identity_file):
        self.identity_file = identity_file
        self.state = self.load_identity()

    def load_identity(self):
        """Charge l'état d'identité créé par Levite"""
        try:
            with open(self.identity_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "identity": data.get("identity", {}),
                    "version": data.get("version", 0),
                    "history": data.get("history", [])
                }
        except FileNotFoundError:
            return {"identity": {}, "version": 0, "history": []}

    def respond(self, question):
        """
        Rejeu mécanique depuis l'état
        Pas de synthèse globale, seulement reformulation locale
        """
        q = question.lower().strip()
        
        # Rejeu mécanique de l'identité
        if "qui es-tu" in q or "qui es tu" in q:
            return self.replay_identity()
        
        # Rejeu du nom
        if "nom" in q:
            return self.replay_key("name")
        
        # Rejeu brut de toutes les déclarations
        if "dis-moi tout" in q or "dis moi tout" in q:
            return self.replay_all()
        
        # Rejeu des contradictions
        if "contradictions" in q:
            return self.replay_contradictions()
        
        # Défaut : état vide
        return "je ne sais pas"

    def replay_identity(self):
        """
        Rejoue la dernière déclaration d'identité
        Reformulation locale cohérente sans synthèse globale
        """
        identity = self.state["identity"]
        if not identity:
            return "je ne sais rien"
        
        # Récupère les déclarations d'état
        declarations = [v for k, v in identity.items() if k.startswith("q_") and "state" in k]
        if declarations:
            return declarations[-1]  # Dernière déclaration
        
        return "je ne sais pas"

    def replay_key(self, key):
        """Rejoue une clé spécifique de l'identité"""
        identity = self.state["identity"]
        if key in identity:
            return identity[key]
        return "je ne sais pas"

    def replay_all(self):
        """
        Rejeu brut sans synthèse
        Liste tous les états stockés
        """
        identity = self.state["identity"]
        if not identity:
            return "rien"
        
        # Rejeu brut de tous les états
        output = []
        for key, value in identity.items():
            output.append(f"{key}: {value}")
        return "\n".join(output)

    def replay_contradictions(self):
        """
        Rejoue les contradictions détectées par Levite
        Sans résolution, juste exposition
        """
        history = self.state["history"]
        contradictions = [e for e in history if e.get("contradiction")]
        
        if not contradictions:
            return "aucune contradiction enregistrée"
        
        # Rejeu brut des contradictions
        output = []
        for c in contradictions:
            output.append(f"[{c['question_id']}] {c['previous']} → {c['value']}")
        return "\n".join(output)

if __name__ == "__main__":
    adam = Adam(IDENTITY_FILE)
    
    if adam.state["version"] == 0:
        print("[ADAM : AUCUNE IDENTITÉ CHARGÉE]")
        print("[ADAM : EXÉCUTER LEVITE D'ABORD]\n")
    else:
        print(f"[ADAM : VERSION {adam.state['version']} CHARGÉE]")
        print(f"[ADAM : {len(adam.state['identity'])} ÉTATS DISPONIBLES]\n")
    
    print("Commandes :")
    print("  - qui es-tu")
    print("  - dis-moi tout")
    print("  - contradictions")
    print("  - exit\n")
    
    while True:
        question = input("Yehi>> ")
        if question.lower() == "exit":
            break
        response = adam.respond(question)
        print(response)
        print()