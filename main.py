import subprocess

def connect_elijah():
    print("\nConnexion à Elijah...\n")
    subprocess.run(["python", "elijah/elijah.py"])

def connect_adam():
    print("\nConnexion à Adam...\n")
    subprocess.run(["python", "adam/adam.py"])

def explain_wtf():
    print("""
XNO MITOSIS : WTF IS THAT ?

Elijah :
Pose des questions.

Levite :
Invisible ici.

Adam :
Ton clone qui répond aux questions en se basant sur l’identité que Levite a construite à partir des réponses données à Elijah.

Si ça te met mal à l’aise,
c’est normal.
""")

def main():
    while True:
        print("\nA qui voulez-vous vous connecter ?")
        print("[1] Elijah")
        print("[2] Adam")
        print("[3] Sortir")
        print("[4] WTF is that ?")

        choice = input("> ").strip()

        if choice == "1":
            connect_elijah()
        elif choice == "2":
            connect_adam()
        elif choice == "3":
            print("Sortie.")
            break
        elif choice == "4":
            explain_wtf()
        else:
            print("nenon ! tu t'es trompé de touche ! :)")

if __name__ == "__main__":
    main()
