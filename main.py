def main():
    print("XNO MITOSIS")
    print("[1] Mode classique (CLI)")
    print("[2] Mode interface (TUI 2000s)")
    print("[3] Quitter")

    choice = input("> ").strip()

    if choice == "1":
        run_cli()
    elif choice == "2":
        from tui_curses import run_curses
        run_curses()
    else:
        print("Sortie.")


def run_cli():
    from elijah.elijah import Elijah
    from adam.adam import Adam

    elijah = Elijah()
    adam = Adam()

    while True:
        print("\n[1] Elijah")
        print("[2] Adam")
        print("[3] Quitter")
        c = input("> ").strip()

        if c == "1":
            for q_id, question in elijah.ask():
                print(f"ELIJAH > {question}")
                ans = input("> ")
                elijah.save_response(q_id, question, ans)

        elif c == "2":
            while True:
                q = input("ADAM > ")
                if q == "exit":
                    break
                print("ADAM >", adam.respond(q))

        elif c == "3":
            break


if __name__ == "__main__":
    main()
