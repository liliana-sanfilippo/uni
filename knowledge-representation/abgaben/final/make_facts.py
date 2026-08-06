import json

fakten = []

with open("all_data.json", 'r') as file:
    module_data = json.load(file)

    for module in module_data:
        fakten.append(f'(modul (id "{module["kuerzel"]}") (lp {module["lp"]}) (dauer {module["dauer"]}))')
        for mod_ver in module["veranstaltungen"]:
            fakten.append(f'(modell_veranstaltung (id {mod_ver["uni_id"]}) (modul "{module["kuerzel"]}") (typ {mod_ver["type"]}))')


with open("fakten.txt", "w") as text_file:
    text_file.write(str(fakten))


    print(fakten)