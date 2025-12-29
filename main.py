import subprocess
import os
import time
import sys
import json
from datetime import datetime

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

class TUILayout:
    def __init__(self):
        self.width = 180
        self.left_width = 50
        self.center_width = 80
        self.right_width = 40
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_border(self, width, color=Colors.CYAN):
        return f"{color}{'═' * width}{Colors.RESET}"
    
    def draw_header(self):
        header = "X N O   M I T O S I S   I N T E R F A C E"
        padding = (self.width - len(header)) // 2
        print(f"\n{Colors.CYAN}╔{'═' * self.width}╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}{' ' * padding}{Colors.BOLD}{Colors.WHITE}{header}{Colors.RESET}{' ' * (self.width - padding - len(header))}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚{'═' * self.width}╝{Colors.RESET}\n")
    
    def draw_three_panel_start(self):
        print(f"{Colors.CYAN}╔{'═' * self.left_width}╦{'═' * self.center_width}╦{'═' * self.right_width}╗{Colors.RESET}")
    
    def draw_three_panel_row(self, left, center, right):
        left_pad = self.left_width - len(self.strip_ansi(left))
        center_pad = self.center_width - len(self.strip_ansi(center))
        right_pad = self.right_width - len(self.strip_ansi(right))
        
        print(f"{Colors.CYAN}║{Colors.RESET}{left}{' ' * left_pad}{Colors.CYAN}║{Colors.RESET}{center}{' ' * center_pad}{Colors.CYAN}║{Colors.RESET}{right}{' ' * right_pad}{Colors.CYAN}║{Colors.RESET}")
    
    def draw_three_panel_separator(self):
        print(f"{Colors.CYAN}╠{'═' * self.left_width}╬{'═' * self.center_width}╬{'═' * self.right_width}╣{Colors.RESET}")
    
    def draw_three_panel_end(self):
        print(f"{Colors.CYAN}╚{'═' * self.left_width}╩{'═' * self.center_width}╩{'═' * self.right_width}╝{Colors.RESET}")
    
    def strip_ansi(self, text):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

class ConsoleManager:
    def __init__(self, max_lines=20):
        self.logs = []
        self.max_lines = max_lines
    
    def add_log(self, text, log_type='info'):
        color_map = {
            'info': Colors.GRAY,
            'success': Colors.GREEN,
            'error': Colors.RED,
            'warning': Colors.YELLOW,
            'user': Colors.CYAN
        }
        color = color_map.get(log_type, Colors.GRAY)
        self.logs.append(f"{color}{text}{Colors.RESET}")
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
    
    def get_logs(self):
        return self.logs

class MessageManager:
    def __init__(self, max_lines=15):
        self.messages = []
        self.max_lines = max_lines
    
    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)
    
    def get_messages(self):
        return self.messages

class XnoMitosisTUI:
    def __init__(self):
        self.layout = TUILayout()
        self.console = ConsoleManager()
        self.messages = MessageManager()
        self.active_module = None
        self.entity_name = "SYSTÈME"
        
        # Module data
        self.elijah_session = None
        self.levite_state = None
        
    def render(self):
        self.layout.clear_screen()
        self.layout.draw_header()
        
        # Draw menu section
        self.layout.draw_three_panel_start()
        self.layout.draw_three_panel_row(
            f"{Colors.BOLD}MENU{Colors.RESET}".center(50),
            f"{Colors.BOLD}nom de l'entité [ {self.entity_name} ]{Colors.RESET}",
            f"{Colors.BOLD}sortie console{Colors.RESET}"
        )
        self.layout.draw_three_panel_separator()
        
        # Menu items
        menu_items = [
            f"{Colors.GREEN}[1]{Colors.RESET} → ELIJAH  {Colors.GRAY}│ Questionnement séquentiel{Colors.RESET}",
            f"{Colors.MAGENTA}[2]{Colors.RESET} → LEVITE  {Colors.GRAY}│ Traitement d'identité{Colors.RESET}",
            f"{Colors.YELLOW}[3]{Colors.RESET} → ADAM    {Colors.GRAY}│ Rejeu cognitif{Colors.RESET}",
            f"{Colors.BLUE}[4]{Colors.RESET} → WTF     {Colors.GRAY}│ Documentation système{Colors.RESET}",
            f"{Colors.RED}[5]{Colors.RESET} → EXIT    {Colors.GRAY}│ Déconnexion{Colors.RESET}",
        ]
        
        # Get messages and console logs
        messages = self.messages.get_messages()
        logs = self.console.get_logs()
        
        max_rows = max(len(menu_items), len(messages), len(logs))
        
        for i in range(max_rows):
            left = menu_items[i] if i < len(menu_items) else ""
            
            # Center (messages)
            if i < len(messages):
                msg = messages[i]
                if msg['role'] == 'agent':
                    center = f"{Colors.CYAN}agent> {Colors.WHITE}{msg['content'][:70]}{Colors.RESET}"
                elif msg['role'] == 'user':
                    center = f"{Colors.YELLOW}user> {Colors.WHITE}{msg['content'][:70]}{Colors.RESET}"
                else:
                    center = f"{Colors.GRAY}{msg['content'][:70]}{Colors.RESET}"
            else:
                center = ""
            
            # Right (console)
            right = logs[i] if i < len(logs) else ""
            
            self.layout.draw_three_panel_row(left, center, right)
        
        self.layout.draw_three_panel_separator()
        
        # File tree
        file_tree = [
            f"{Colors.GRAY}xno_mitosis/{Colors.RESET}",
            "├── main.py",
            "├── elijah/",
            "│   ├── elijah.py",
            "│   └── responses/",
            "├── levite/",
            "│   ├── levite.py",
            "│   └── identity_state.json",
            "└── adam/",
            "    └── adam.py",
        ]
        
        for i, line in enumerate(file_tree):
            self.layout.draw_three_panel_row(
                f"{Colors.GRAY}{line}{Colors.RESET}",
                "",
                ""
            )
        
        self.layout.draw_three_panel_end()
        
        print(f"\n{Colors.CYAN}>>> {Colors.RESET}", end='')
    
    def run_elijah(self):
        self.active_module = 'elijah'
        self.entity_name = 'ELIJAH'
        self.console.add_log('>>> CONNEXION À ELIJAH', 'success')
        self.console.add_log('[SESSION INITIALISÉE]', 'info')
        self.messages.add_message('system', 'Session Elijah démarrée')
        
        # Import and run elijah module
        from elijah.elijah import Elijah
        elijah = Elijah("elijah/elijah_questions.json")
        
        self.render()
        
        # Interactive questioning
        for q_data in elijah.questions:
            self.messages.add_message('agent', q_data['text'])
            self.render()
            answer = input()
            self.messages.add_message('user', answer)
            elijah.save_response(q_data['id'], q_data['text'], answer)
            self.console.add_log(f"[Q{q_data['id']}] SAVED", 'success')
        
        self.console.add_log(f'[SESSION TERMINÉE: {elijah.session_id}]', 'success')
        self.elijah_session = elijah.session_id
        
        input(f"\n{Colors.GRAY}[Appuyer sur ENTRÉE pour continuer]{Colors.RESET}")
    
    def run_levite(self):
        if not self.elijah_session:
            self.console.add_log('[ERREUR: Aucune session Elijah]', 'error')
            self.messages.add_message('system', 'Exécutez d\'abord Elijah')
            self.render()
            input()
            return
        
        self.active_module = 'levite'
        self.entity_name = 'LEVITE'
        self.console.add_log('>>> CONNEXION À LEVITE', 'success')
        
        from levite.levite import Levite
        levite = Levite()
        
        session_path = os.path.join("elijah/responses", self.elijah_session)
        
        if os.path.exists(session_path):
            self.console.add_log(f'[TRAITEMENT SESSION {self.elijah_session}]', 'info')
            levite.process_session(session_path)
            self.console.add_log(f"[VERSION {levite.state['version']} ENREGISTRÉE]", 'success')
            self.console.add_log(f"[{len(levite.state['history'])} ÉVÉNEMENTS]", 'info')
            self.messages.add_message('system', f"Traitement terminé. Version {levite.state['version']}")
            self.levite_state = levite.state
        
        self.render()
        input(f"\n{Colors.GRAY}[Appuyer sur ENTRÉE pour continuer]{Colors.RESET}")
    
    def run_adam(self):
        if not self.levite_state or self.levite_state['version'] == 0:
            self.console.add_log('[AVERTISSEMENT: Identité non construite]', 'warning')
        
        self.active_module = 'adam'
        self.entity_name = 'ADAM'
        self.console.add_log('>>> CONNEXION À ADAM', 'success')
        
        from adam.adam import Adam
        adam = Adam("levite/identity_state.json")
        
        if adam.state['version'] > 0:
            self.console.add_log(f"[VERSION {adam.state['version']} CHARGÉE]", 'success')
            self.console.add_log(f"[{len(adam.state['identity'])} ÉTATS]", 'info')
            self.messages.add_message('system', 'Commandes: qui es-tu, dis-moi tout, contradictions, exit')
        
        while True:
            self.render()
            question = input()
            
            if question.lower() == 'exit':
                break
            
            self.messages.add_message('user', question)
            response = adam.respond(question)
            self.messages.add_message('agent', response)
            self.console.add_log('[REPLAY EXÉCUTÉ]', 'success')
    
    def show_documentation(self):
        self.active_module = 'wtf'
        self.entity_name = 'DOCUMENTATION'
        self.console.add_log('>>> ACCÈS DOCUMENTATION', 'info')
        
        docs = [
            '╔════════════════════════════════════╗',
            'XNO MITOSIS : ARCHITECTURE COGNITIVE',
            '╚════════════════════════════════════╝',
            '',
            '[ELIJAH] → Pose des questions séquentielles',
            '         → Ne valide rien',
            '         → Stocke brut',
            '',
            '[LEVITE] → Traite les réponses d\'Elijah',
            '         → Extrait des états symboliques',
            '         → Préserve les contradictions',
            '',
            '[ADAM]   → Rejoue l\'identité construite',
            '         → Reformule localement',
            '         → Incohérent globalement',
        ]
        
        for doc in docs:
            self.messages.add_message('system', doc)
        
        self.render()
        input(f"\n{Colors.GRAY}[Appuyer sur ENTRÉE pour continuer]{Colors.RESET}")
    
    def run(self):
        while True:
            self.render()
            choice = input().strip()
            
            if choice == '1':
                self.run_elijah()
            elif choice == '2':
                self.run_levite()
            elif choice == '3':
                self.run_adam()
            elif choice == '4':
                self.show_documentation()
            elif choice == '5':
                self.console.add_log('>>> DÉCONNEXION', 'error')
                self.render()
                time.sleep(1)
                break
            else:
                self.console.add_log('[ERREUR: ENTRÉE INVALIDE]', 'error')

if __name__ == "__main__":
    tui = XnoMitosisTUI()
    tui.run()