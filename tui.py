from textual.app import App, ComposeResult
from textual.widgets import Static, ListView, ListItem, Input
from textual.containers import Horizontal, Vertical

from elijah.elijah import Elijah
from levite.levite import Levite
from adam.adam import Adam


class XNOMitosisTUI(App):
    TITLE = "XNO MITOSIS"

    CSS = """
    Screen {
        background: black;
        color: white;
    }

    #left, #center, #right {
        border: solid white;
        padding: 1;
    }

    #left {
        width: 28%;
    }

    #center {
        width: 44%;
    }

    #right {
        width: 28%;
    }

    .dim {
        color: gray;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            # MENU
            with Vertical(id="left"):
                yield Static("XNO MITOSIS", classes="dim")
                self.menu = ListView(
                    ListItem(Static("ELIJAH")),
                    ListItem(Static("ADAM")),
                    ListItem(Static("EXIT")),
                )
                yield self.menu

            # INTERACTION
            with Vertical(id="center"):
                self.interaction = Static("")
                yield self.interaction
                self.input_box = Input()
                yield self.input_box

            # LOG (hostile : presque vide)
            with Vertical(id="right"):
                self.log_panel = Static("READY", classes="dim")
                yield self.log_panel

    def on_mount(self):
        self.xno_entity = None

        self.elijah = Elijah()
        self.levite = Levite()
        self.adam = Adam()

        self.elijah_iter = None
        self._write_log("SYSTEM ONLINE")

    def on_list_view_selected(self, event: ListView.Selected):
        choice = event.item.renderable.plain

        if choice == "ELIJAH":
            self.xno_entity = "ELIJAH"
            self.elijah_iter = self.elijah.ask()
            q_id, question = next(self.elijah_iter)
            self._append(f"ELIJAH > {question}")

        elif choice == "ADAM":
            self.xno_entity = "ADAM"
            self._append("ADAM >")

        elif choice == "EXIT":
            self.exit()

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()
        event.input.value = ""

        if not text:
            return

        self._append(f"user > {text}")

        if self.xno_entity == "ELIJAH":
            self.elijah.save_response("?", "?", text)
            self.levite.process(text)

            try:
                q_id, question = next(self.elijah_iter)
                self._append(f"ELIJAH > {question}")
            except StopIteration:
                self._append("ELIJAH >")

        elif self.xno_entity == "ADAM":
            response = self.adam.respond(text)
            self._append(f"ADAM > {response}")

        else:
            # Hostile silence
            self._append("")

    # ---------- helpers ----------

    def _append(self, line: str):
        current = self.interaction.renderable or ""
        if current:
            self.interaction.update(f"{current}\n{line}")
        else:
            self.interaction.update(line)

    def _write_log(self, msg: str):
        self.log_panel.update(msg)
