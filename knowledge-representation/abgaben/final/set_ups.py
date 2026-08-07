import clips


def set_up_env():
    environment = clips.Environment()
    environment.load("clip_definitionen.clp")
    environment.reset()
    with open("fakten.txt", "r") as text_file:
        fakten = text_file.readlines()
        for f in fakten:
            environment.assert_string(f)
        return environment


def reset_environment_for_clean_answer(environment):
    environment.reset()
    with open("fakten.txt", "r") as text_file:
        fakten = text_file.readlines()
        for f in fakten:
            environment.assert_string(f)
    return environment
