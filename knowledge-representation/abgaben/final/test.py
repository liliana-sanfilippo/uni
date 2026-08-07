from clips_main import get_answer, alle
from helper_functions_printing import answer_string
from set_ups import set_up_env, reset_environment_for_clean_answer


def test_course_to_module(env, kurs, modul, sem):
    env.run()
    treffer = get_answer(env, "gehoert-zu-modul", **{"echte_veranstaltung": kurs, "modul": modul})
    return answer_string(treffer), f'  -> Does course {kurs} belong to module "{modul}"?'


def test_use_course_for_module(env, kurs, modul, sem):
    env.assert_string(f'(frage-belegen (student liliana) '
                      f'(echte_veranstaltung {kurs}) (modul "{modul}"))')
    env.run()
    treffer = get_answer(env, "kann-belegen",
                         **{"student": "liliana", "echte_veranstaltung": kurs, "modul": modul})
    return answer_string(treffer), f'  -> Can liliana choose the course {kurs} for the module "{modul}"?'


def test_do_course_in_semester(env, kurs, modul, sem):
    env.assert_string(f'(frage-belegen-sem (student liliana) '
                      f'(echte_veranstaltung {kurs}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "kann-belegen-sem",
                         **{"student": "liliana", "echte_veranstaltung": kurs, "semester": sem})
    return answer_string(treffer), f"  -> Can liliana choose course {kurs} in {sem}?"


def test_fulfill_prerequisites(env, kurs, modul, sem):
    env.assert_string(f'(frage-belegbar-modul (student liliana) (modul "{modul}"))')
    env.run()
    fehlend = []
    treffer = get_answer(env, "modul-belegbar", **{"student": "liliana", "modul": modul})
    if not treffer:
        fehlend = alle(env, "fehlende-voraussetzung", **{"student": "liliana", "modul": modul})

    return len(fehlend), f'  -> Can liliana do the module "{modul}"?'


def test_complete_module_one_semester(env, kurs, modul, sem):
    env.assert_string(f'(frage-abschluss-sem (modul "{modul}") (semester {sem}))')
    env.run()
    treffer = get_answer(env, "modul-abschliessbar-sem", **{"modul": modul, "semester": sem})
    return answer_string(treffer), f'  -> Can the module "{modul}" be completed in one {sem}?'


def test_modul_abgeschlossen(env, kurs, modul, sem):
    env.run()
    treffer = get_answer(env, "modul-abgeschlossen", **{"student": "liliana", "modul": modul})
    return answer_string(treffer), f' -> Has liliana completed the module "{modul}"?'


def set_up_scenario(filename, environment):
    env = reset_environment_for_clean_answer(environment)
    with open("scenarios/" + filename, "r") as background:
        bg = background.readlines()
        for f in bg:
            env.assert_string(f)
            print(f)
    return env


SCENARIOS = [
    {
        "id": "01",
        "desc": "It is (the start of) the winter semester. The student has not completed any courses yet. They want "
                "to take the module 39-M-Inf-INT-adv_a and are interested in the course Neural Networks Natural "
                "Language Processing (624620553)",
        "module": "39-M-Inf-INT-adv_a",
        "course": 624620553,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "YES",
        "expected_do_course_in_semester": "YES",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO"
    },
    {
        "id": "02",
        "desc": "It is (the start of) the winter semester. The student so far completed the course Neural Networks "
                "Natural Language Processing (624620553). They want to take the module 39-M-Inf-INT-adv_a and are interested "
                "in the course Human Centered Artifical Intelligence Lab ForschKolloq. (659886362). Since they have "
                "taken the course NNNLP already, the module 39-M-Inf-INT-adv_a is completed and they cannot take the "
                "course for that module.",
        "module": "39-M-Inf-INT-adv_a",
        "course": 659886362,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "YES",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "YES"
    },{
        "id": "03",
        "desc": "It is (the start of) the summer semester. The student so far completed the course Neural Networks "
                "Natural Language Processing (624620553) and therefore the module 39-M-Inf-INT-adv_a. They want to take the module "
                "39-M-Inf-INT-app-foc_a, for which 39-M-Inf-INT-adv_a is a prerequisite, and are interested "
                "in the course Intelligent Tutoring Systems (737382051).",
        "module": "39-M-Inf-INT-app-foc_a",
        "course": 737382051,
        "semester": "ss",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "YES",
        "expected_do_course_in_semester": "YES",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO"
    }
]

QUESTIONS = {
    "course_to_module": test_course_to_module,
    "use_course_for_module": test_use_course_for_module,
    "do_course_in_semester": test_do_course_in_semester,
    "fulfill_prerequisites": test_fulfill_prerequisites,
    "complete_module_one_semester": test_complete_module_one_semester,
    "modul_abgeschlossen": test_modul_abgeschlossen
}


def main():
    environment = set_up_env()
    with open("test_results.txt", "w") as text_file:
        for scen in SCENARIOS:
            error_occurred = False
            text_file.write("=========================================\n")
            text_file.write(f'TEST SCENARIO {scen["id"]}:\n')
            text_file.write("=========================================\n\n")

            # Set up with discarding old info
            env = set_up_scenario(f'mockup_{scen["id"]}.txt', environment)
            index = 1
            for quest in QUESTIONS:
                function = QUESTIONS[quest]
                real_answer, question_text = function(env, scen["course"], scen["module"], scen["semester"])
                text_file.write(f'Question {index}: {question_text}\n')

                text_file.write(f'Expected answer: {scen[f'expected_{quest}']}\n')
                text_file.write(f'Actual answer:   {real_answer}\n')
                if real_answer != scen[f'expected_{quest}']:
                    error_occurred = True
                    text_file.write(f'\n---> ERROR <---\n')
                index += 1
            if error_occurred:
                print(f'Error in question_text')
                text_file.write("\n\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
                for f in env.facts():
                    text_file.write(f'{f}\n')
                text_file.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")


if __name__ == "__main__":
    main()
