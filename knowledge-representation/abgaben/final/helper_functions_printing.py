
def answer_string(treffer):
    return "YES" if treffer else "NO"

def print_answer(answer):
    print("############")
    print(answer)
    print("############")

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
