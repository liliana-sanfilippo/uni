
import clips


def reset_environment_for_clean_answer(environment):
    environment.reset()
    with open("fakten.txt", "r") as text_file:
        fakten = text_file.readlines()
        for f in fakten:
            environment.assert_string(f)
    return environment

def ask_user(prompt):
    return input(prompt).strip()

def ask_user_for_semester(prompt="  semester (ws/ss): "):
    while True:
        s = input(prompt).strip().lower()
        if s in ("ws", "ss"):
            return s
        print("  Please enter 'ws' oder 'ss'!")

def get_answer(env, template, **slots):
    for f in env.facts():
        #print(f)
        if f.template.name == template and all(str(f[k]) == str(v) for k, v in slots.items()):
            return f
    return None

def answer_string(treffer):
    return "YES" if treffer else "NO"

def print_answer(answer):
    print("############")
    print(answer)
    print("############")

def q_course_to_module(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    modul = ask_user("  module code: ")
    env = reset_environment_for_clean_answer(environment)
    env.run()
    treffer = get_answer(env, "gehoert-zu-modul", **{"echte_veranstaltung": kurs, "modul": modul})
    print_answer(f"  -> Does course {kurs} belong to module {modul}?  {answer_string(treffer)}")


def q_use_course_for_module(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    modul = ask_user("  module code: ")
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-belegen (student liliana) '
                      f'(echte_veranstaltung {kurs}) (modul "{modul}"))')
    env.run()
    treffer = get_answer(env, "kann-belegen",
                    **{"student": "liliana", "echte_veranstaltung": kurs, "modul": modul})
    print_answer(f"  -> Can liliana choose the course {kurs} for the module {modul}?  {answer_string(treffer)}")


def q_do_course_in_semester(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    sem = ask_user_for_semester()
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-belegen-sem (student liliana) '
                      f'(echte_veranstaltung {kurs}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "kann-belegen-sem",
                         **{"student": "liliana", "echte_veranstaltung": kurs, "semester": sem})
    print_answer(f"  -> Can liliana choose course {kurs} in {sem.upper()}?  {answer_string(treffer)}")



FRAGEN = {
    "1": ("Does a course belong to a module?",              q_course_to_module),
    "2": ("Can I choose a course for a module?",   q_use_course_for_module),
    "3": ("Can I do a course in a semester?", q_do_course_in_semester)
}


def set_up_env():
    environment = clips.Environment()
    environment.load("clip_definitionen.clp")
    environment.reset()
    with open("fakten.txt", "r") as text_file:
        fakten = text_file.readlines()
        for f in fakten:
            environment.assert_string(f)
        return environment


def scenario(filename):
    environment = set_up_env()
    with open("scenarios/" + filename, "r") as background:
        bg = background.readlines()

    for f in bg:
        environment.assert_string(f)

    environment.run()


def run_tests():
    scenario("mockup_01.txt")
    scenario("mockup_02.txt")
    scenario("mockup_03.txt")
    scenario("mockup_04.txt")
    scenario("mockup_05.txt")
    scenario("mockup_06.txt")
    scenario("mockup_07.txt")
    scenario("mockup_08.txt")
    scenario("mockup_09.txt")
    scenario("mockup_10.txt")


def alle(env, template, **slots):
    return [f for f in env.facts()
            if f.template.name == template and all(str(f[k]) == str(v) for k, v in slots.items())]


def list_modules_and_courses(environment):
    print("\n  Modules:")
    for f in sorted(alle(environment, "modul"), key=lambda x: str(x['id'])):
        print(f"    {f['id']}  (pr={f['pr']}, sl={f['sl']})")
    print("  Courses (echte_veranstaltung):")
    gesehen = set()
    for f in alle(environment, "echte_veranstaltung"):
        if f['id'] not in gesehen:
            gesehen.add(f['id'])
            print(f"    {f['id']}  {f['titel']}")
    print()



def main():
    environment = set_up_env()
    while True:
        print("Hello, please choose your question")
        for k, (text, _) in FRAGEN.items():
            print(f"  {k}) {text}")
        print("  l) Show modules and courses")
        print("  t) Run test scenarios")
        print("  q) Exit")
        choice = input("Choice: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Exiting...")
            break
        if choice == "l":
            list_modules_and_courses(environment)
            print("Please copy a module code or a course ID to use in your questions.")
            print("")
            con = input("Continue? (y/n) ").strip().lower()
            if con in ("yes", "y"):
                continue
            else:
                print("Exiting...")
                break
        if choice in FRAGEN:
            _, funktion = FRAGEN[choice]
            try:
                funktion(environment)
                con = input("Continue? (y/n) ").strip().lower()
                if con in ("yes", "y"):
                    continue
                else:
                    print("Exiting...")
                    break
            except Exception as e:
                print(f"  Fehler bei der Anfrage: {e}")






if __name__ == "__main__":
    main()
