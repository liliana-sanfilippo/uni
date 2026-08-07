import clips

from helper_functions_printing import print_answer, answer_string, list_modules_and_courses, alle
from helper_functions_user_input import ask_user, ask_user_for_semester, ask_user_for_program
from set_ups import set_up_env, reset_environment_for_clean_answer


def get_answer(env, template, **slots):
    for f in env.facts():
        if f.template.name == template and all(str(f[k]) == str(v) for k, v in slots.items()):
            return f
    return None


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
    print_answer(f"  -> Can I choose the course {kurs} for the module {modul}?  {answer_string(treffer)}")


def q_do_course_in_semester(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    sem = ask_user_for_semester()
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-belegen-sem (student liliana) '
                      f'(echte_veranstaltung {kurs}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "kann-belegen-sem",
                         **{"student": "liliana", "echte_veranstaltung": kurs, "semester": sem})
    print_answer(f"  -> Can I choose course {kurs} in {sem.upper()}?  {answer_string(treffer)}")

def q_course_available_in_semester(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    sem = ask_user_for_semester()
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-in-semester-vorhanden '
                      f'(echte_veranstaltung {kurs}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "in-sem-vorhanden",
                         **{"echte_veranstaltung": kurs, "semester": sem})
    print_answer(f"  -> Is the course {kurs} available in {sem}?    {answer_string(treffer)}")


def q_fulfill_prerequisites(environment):
    modul = ask_user("  module code: ")
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-belegbar-modul (student liliana) (modul {modul})')
    env.run()
    treffer = get_answer(env, "modul-belegbar", **{"student": "liliana", "modul": modul})
    print_answer(f"  -> Do I fulfill the prerequisites for the module {modul}?  {answer_string(treffer)}")
    if not treffer:
        fehlend = alle(env, "fehlende-voraussetzung", **{"student": "liliana", "modul": modul})
        for f in fehlend:
            print(f"     Missing prerequisites: {f['benoetigt']}")


def q_complete_module_one_semester(environment):
    modul = ask_user("  module code: ")
    sem = ask_user_for_semester()
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-abschluss-sem (modul {modul}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "modul-abschliessbar-sem", **{"modul": modul, "semester": sem})
    print_answer(f"  -> Can the module {modul} be completed in one {sem.upper()}? "
                 f" {answer_string(treffer)}")

def q_course_for_program(environment):
    kurs = ask_user("  course_id (echte_veranstaltung): ")
    program = ask_user_for_program()
    env = reset_environment_for_clean_answer(environment)
    env.assert_string(f'(frage-kurs-programm (echte_veranstaltung {kurs}) (programm {program.upper()}))')
    treffer = get_answer(env, "kurs-fuer-programm",
                    **{"echte_veranstaltung": kurs, "programm": program.upper()})
    print(f'  -> Can course {kurs} be studied for program {program.upper()}?  {answer_string(treffer)}')



def q_modul_abgeschlossen(environment):
    modul = ask_user("  module code: ")
    env = reset_environment_for_clean_answer(environment)
    env.run()
    treffer = get_answer(env, "modul-abgeschlossen", **{"student": "liliana", "modul": modul})
    print_answer(f"  -> Have I completed the module {modul}?  {answer_string(treffer)}")



FRAGEN = {
    "1": ("Does a course belong to a module?", q_course_to_module),
    "2": ("Can I choose a course for a module?", q_use_course_for_module),
    "3": ("Can I choose a course in a semester?", q_do_course_in_semester),
    "4": ("Do I fulfill the prerequisites for a module?", q_fulfill_prerequisites),
    "5": ("Can a module be completed in one semester?", q_complete_module_one_semester),
    "6": ("Have I completed a module?", q_modul_abgeschlossen),
    "7": ("Is a course available in a semester?", q_course_available_in_semester),
    "8": ("Can a course be chosen for a program?", q_course_for_program)
}


def main():
    environment = set_up_env()
    while True:
        print("Hello, please choose your question")
        for k, (text, _) in FRAGEN.items():
            print(f"  {k}) {text}")
        print("  l) Show modules and courses")
        print("  t) Run test scenarios")
        print("  q) Exit")
        #print("  e) I want to enter information")
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
        if choice == "e":
            while True:
                print("  A.) I want to enter a course (echte_veranstaltung) I completed")
                print("  B.) I want to assign a course to a module")
                print("  q) Go back")
                sec_choice = input("Choice: ").strip().lower()
                if sec_choice in ("q", "quit", "exit"):
                    print("Back to main menu...")
                    break
                if con in ("yes", "y"):
                    continue
                else:
                    print("Exiting...")
                    break


if __name__ == "__main__":
    main()
