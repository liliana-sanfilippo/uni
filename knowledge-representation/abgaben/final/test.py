from clips_main import get_answer
from helper_functions_printing import answer_string, alle
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


def test_course_available_in_semester(env, kurs, modul, sem):
    env.assert_string(f'(frage-in-semester-vorhanden '
                      f'(echte_veranstaltung {kurs}) (semester {sem}))')
    env.run()
    treffer = get_answer(env, "in-sem-vorhanden",
                         **{"echte_veranstaltung": kurs, "semester": sem})
    return answer_string(treffer), f"  -> Is the course {kurs} available in {sem}?"


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


def set_up_scenario(filename, env):
    env = reset_environment_for_clean_answer(env)
    with open("scenarios/" + filename, "r") as background:
        bg = background.readlines()
        for f in bg:
            env.assert_string(f)
            #print(f)
    return env


SCENARIOS = [
    {
        "id": "01",
        "mockup": "01",
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
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },
    {
        "id": "02",
        "mockup": "02",
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
        "expected_modul_abgeschlossen": "YES",
        "expected_course_available_in_semester": "YES"
    },{
        "id": "03",
        "mockup": "03",
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
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },{
        "id": "04",
        "mockup": "04",
        "desc": "It is (the start of) the winter semester. \n"
                "The student so far completed no courses They want to take the module 39-M-Inf-INT-app-foc_a, for which 39-M-Inf-INT-adv_a is a prerequisite, and are interested "
                "in the course Intelligent Tutoring Systems (737382051), which is offered in the summer semester.",
        "module": "39-M-Inf-INT-app-foc_a",
        "course": 737382051,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "YES",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 1,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "NO"
    },
    {
        "id": "05",
        "mockup": "05",
        "desc": """It is (the start of) the summer semester. \n 
                The student already took the courses Agentic AI Architectures Self Evolution Safety (659862590) and 
                the course Neural Networks Natural Language Processing (624620553) due to which the module 
                39-M-Inf-INT-adv_a is completed.\n
                They are interested in the course (Privacy Healthcare 662782877) which is offered in the winter 
                semester and want to take the module 39-M-Inf-INT-app-foc_a which has the 
                prerequisites 39-M-Inf-INT-app and 39-M-Inf-INT-adv_a.
                """,
        "module": "39-M-Inf-INT-app-foc_a",
        "course": 662782877,
        "semester": "ss",
        "expected_course_to_module": "NO",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 1,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "NO"
    },
    {
        "id": "06",
        "mockup": "06",
        "desc": """It is (the start of) the winter semester. \n 
                The student already took the courses Agentic AI Architectures Self Evolution Safety (659862590). \n
                They are interested in the course (Privacy Healthcare 662782877) which is offered in the winter 
                semester and want to take the module 39-M-Inf-INT-app-foc_a which has the 
                prerequisites 39-M-Inf-INT-app and 39-M-Inf-INT-adv_a.
                """,
        "module": "39-M-Inf-INT-app-foc_a",
        "course": 662782877,
        "semester": "ws",
        "expected_course_to_module": "NO",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "YES",
        "expected_fulfill_prerequisites": 2,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },
    {
        "id": "06.1",
        "mockup": "06",
        "desc": """(Variation of the test before) It is (the start of) the winter semester. \n 
                The student already took the courses Agentic AI Architectures Self Evolution Safety (659862590). \n
                They are interested in the course Robot Learning Age Foundation Models (659890294) which is offered 
                in the winter semester and want to take the module 39-M-Inf-INT-app-foc_a which has the 
                prerequisites 39-M-Inf-INT-app and 39-M-Inf-INT-adv_a.
                """,
        "module": "39-M-Inf-INT-app-foc_a",
        "course": 659890294,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "YES",
        "expected_do_course_in_semester": "YES",
        "expected_fulfill_prerequisites": 2,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },
    {
        "id": "07",
        "mockup": "07",
        "desc": """It is (the start of) the winter semester. \n 
                The student already took the course Human Centered Artifical Intelligence Lab ForschKolloq. (
                659886362) which can belong to multiple modules. Since it was already taken but not assigned, 
                they cannot (again) take it for a module, but also have not completed any of the modules the course 
                can be assigned to.
                """,
        "module": ["39-M-Inf-INT-adv_a", "39-M-Inf-AI-adv_a"],
        "course": 659886362,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },
    {
        "id": "08",
        "mockup": "08",
        "desc": """It is (the start of) the winter semester. \n 
                The student already took the course Human Centered Artifical Intelligence Lab ForschKolloq. (
                659886362) which can belong to multiple modules. But the student has attributed it to the 
                39-M-Inf-INT-adv_a module and can therefore not choose it for that module again.
                """,
        "module": "39-M-Inf-AI-adv_a",
        "course": 659886362,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "YES",
        "expected_course_available_in_semester": "YES"
    },{
        "id": "09",
        "mockup": "09",
        "desc": """It is (the start of) the winter semester. \n 
                The student already took the course Human Centered Artifical Intelligence Lab ForschKolloq. (
                659886362) which can belong to multiple modules. The student has assigned it to 39-M-Inf-INT-adv-foc 
                and is checking, if the have completed the modules 39-M-Inf-INT-adv_a or 39-M-Inf-AI-adv_a. 
                """,
        "module": ["39-M-Inf-INT-adv_a", "39-M-Inf-AI-adv_a"],
        "course": 659886362,
        "semester": "ws",
        "expected_course_to_module": "YES",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "YES",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "YES"
    },
    {
        "id": "10",
        "mockup": "01",
        "desc": """It is (the start of) the summer semester. \n 
                The student took no courses so far. \n 
                They are interested in the course (Privacy Healthcare 662782877) which is offered in the winter 
                semester and want to take the module 39-M-Inf-AI-x.
                """,
        "module": "39-M-Inf-AI-x",
        "course": 662782877,
        "semester": "ss",
        "expected_course_to_module": "NO",
        "expected_use_course_for_module": "NO",
        "expected_do_course_in_semester": "NO",
        "expected_fulfill_prerequisites": 0,
        "expected_complete_module_one_semester": "NO",
        "expected_modul_abgeschlossen": "NO",
        "expected_course_available_in_semester": "NO"
    },

]

QUESTIONS = {
    "course_to_module": test_course_to_module,
    "use_course_for_module": test_use_course_for_module,
    "do_course_in_semester": test_do_course_in_semester,
    "fulfill_prerequisites": test_fulfill_prerequisites,
    "complete_module_one_semester": test_complete_module_one_semester,
    "modul_abgeschlossen": test_modul_abgeschlossen,
    "course_available_in_semester": test_course_available_in_semester
}


def main():
    env = set_up_env()
    with open("test_results.txt", "w") as text_file:
        for scen in SCENARIOS:
            error_occurred = False
            text_file.write("=========================================\n")
            text_file.write(f'TEST SCENARIO {scen["id"]}:\n')
            text_file.write("=========================================\n\n")

            # Set up with discarding old info
            env = set_up_scenario(f'mockup_{scen["mockup"]}.txt', env)
            index = 1
            for quest in QUESTIONS:
                function = QUESTIONS[quest]
                if isinstance(scen["module"], str):
                    real_answer, question_text = function(env, scen["course"], scen["module"], scen["semester"])
                    text_file.write(f'Question {index}: {question_text}\n')

                    text_file.write(f'Expected answer: {scen[f'expected_{quest}']}\n')
                    text_file.write(f'Actual answer:   {real_answer}\n')
                    if real_answer != scen[f'expected_{quest}']:
                        error_occurred = True
                        text_file.write(f'\n---> ERROR <---\n')
                else:
                    for jedes_modul in scen["module"]:
                        real_answer, question_text = function(env, scen["course"], jedes_modul, scen["semester"])
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
