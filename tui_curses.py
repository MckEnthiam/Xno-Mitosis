import curses

from elijah.elijah import Elijah
from levite.levite import Levite
from adam.adam import Adam


MENU_ITEMS = [
    "ELIJAH",
    "ADAM",
    "EXIT"
]


class XNOMitosisCurses:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selected = 0
        self.active_entity = None

        self.elijah = Elijah()
        self.levite = Levite()
        self.adam = Adam()
        self.elijah_iter = None

        self.log_lines = ["SYSTEM READY"]
        self.chat_lines = []

    # ---------- DRAW ----------

    def draw_box(self, y, x, h, w, title=""):
        self.stdscr.addstr(y, x, "+" + "-" * (w - 2) + "+")
        for i in range(1, h - 1):
            self.stdscr.addstr(y + i, x, "|" + " " * (w - 2) + "|")
        self.stdscr.addstr(y + h - 1, x, "+" + "-" * (w - 2) + "+")

        if title:
            self.stdscr.addstr(y, x + 2, f"[ {title} ]")

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # Left menu
        self.draw_box(0, 0, h, 25, "MENU")
        for i, item in enumerate(MENU_ITEMS):
            marker = ">" if i == self.selected else " "
            self.stdscr.addstr(2 + i, 2, f"{marker} {item}")

        # Center interaction
        self.draw_box(0, 25, h, w - 50, "INTERACTION")
        for i, line in enumerate(self.chat_lines[-(h - 4):]):
            self.stdscr.addstr(2 + i, 27, line[:w - 54])

        # Right log
        self.draw_box(0, w - 25, h, 25, "LOG")
        for i, line in enumerate(self.log_lines[-(h - 4):]):
            self.stdscr.addstr(2 + i, w - 23, line[:21])

        self.stdscr.refresh()

    # ---------- INPUT ----------

    def input_line(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(h - 2, 27, "> ")
        curses.echo()
        text = self.stdscr.getstr(h - 2, 29, w - 32).decode("utf-8")
        curses.noecho()
        return text.strip()

    # ---------- LOGIC ----------

    def append_chat(self, text):
        self.chat_lines.append(text)

    def append_log(self, text):
        self.log_lines.append(text)

    def select_menu(self):
        choice = MENU_ITEMS[self.selected]

        if choice == "ELIJAH":
            self.active_entity = "ELIJAH"
            self.elijah_iter = self.elijah.ask()
            q_id, question = next(self.elijah_iter)
            self.append_chat(f"ELIJAH > {question}")

        elif choice == "ADAM":
            self.active_entity = "ADAM"
            self.append_chat("ADAM >")

        elif choice == "EXIT":
            raise SystemExit

    def handle_input(self, text):
        self.append_chat(f"user > {text}")

        if self.active_entity == "ELIJAH":
            self.elijah.save_response("?", "?", text)
            self.levite.process(text)

            try:
                q_id, question = next(self.elijah_iter)
                self.append_chat(f"ELIJAH > {question}")
            except StopIteration:
                self.append_chat("ELIJAH >")

        elif self.active_entity == "ADAM":
            response = self.adam.respond(text)
            self.append_chat(f"ADAM > {response}")

    # ---------- LOOP ----------

    def run(self):
        curses.curs_set(0)

        while True:
            self.draw()
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.selected = (self.selected - 1) % len(MENU_ITEMS)

            elif key == curses.KEY_DOWN:
                self.selected = (self.selected + 1) % len(MENU_ITEMS)

            elif key in [10, 13]:
                self.select_menu()

            elif key == ord(">") or key == ord("\n"):
                text = self.input_line()
                if text:
                    self.handle_input(text)


def run_curses():
    curses.wrapper(lambda stdscr: XNOMitosisCurses(stdscr).run())
