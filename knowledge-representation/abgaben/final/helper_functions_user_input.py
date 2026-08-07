def ask_user(prompt):
    return input(prompt).strip()


def ask_user_for_semester(prompt="  semester (ws/ss): "):
    while True:
        s = input(prompt).strip().lower()
        if s in ("ws", "ss"):
            return s
        print("  Please enter 'ws' oder 'ss'!")


def ask_user_for_program(prompt="  program (iisy/nwi): "):
    while True:
        s = input(prompt).strip().lower()
        if s in ("iisy", "nwi"):
            return s
        print("  Please enter 'iisy' oder 'nwi'!")
