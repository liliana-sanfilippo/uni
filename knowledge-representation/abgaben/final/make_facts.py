import json

with open("all_data_manually_completed.json", 'r') as file:
    module_data = json.load(file)
    with open("fakten.txt", "w") as text_file:

        for module in module_data:
            leistungen = module["struktur"].replace(" ", "").split(",")
            sl = 0
            pr = 0
            for leist in leistungen:
                if "SL" in leist:
                    sl = int(leist[0])
                if "Pr" in leist:
                    pr = int(leist[0])

            text_file.write(f'(modul (id "{module["kuerzel"]}") (lp {module["lp"]}) (dauer {module["dauer"]}) (pr '
                            f'{pr}) (sl {sl}))\n')
            for prog in module["programs"]:
                text_file.write(f'(in-program (modul "{module["kuerzel"]}") (programm {prog}))\n')
            for mod_ver in module["veranstaltungen"]:
                if mod_ver["type"] != "Übung":
                    text_file.write(f'(theorie_veranstaltung (id {mod_ver["uni_id"]}) (modul "{module["kuerzel"]}") (typ '
                                    f'"{mod_ver["type"]}"))\n')


                    # Leistungen einlesen
                    if "leistungen" in mod_ver:
                        for lei in mod_ver["leistungen"]:
                            if lei["type"] == "pr":
                                text_file.write(f'(hat-pr (theorie_veranstaltung {mod_ver["uni_id"]}))\n')
                            else:
                                text_file.write(f'(hat-sl (theorie_veranstaltung {mod_ver["uni_id"]}))\n')

                    # reale Kurse hinzufügen
                    ## WS
                    for ws_kurs in mod_ver["kurse"]["ws"]:
                        text_file.write(f'(echte_veranstaltung (id {ws_kurs["uni_id"]}) (typ "{mod_ver["type"]}")  (titel '
                                        f'"{ws_kurs["name"].replace("'", "")}"))\n')
                        text_file.write(f'(instance-of (echte_veranstaltung {ws_kurs["uni_id"]}) ('
                                        f'theorie_veranstaltung {mod_ver["uni_id"]}) (semester '
                                        f'ws))\n')
                    ## SS
                    for ss_kurs in mod_ver["kurse"]["ss"]:
                        text_file.write(f'(echte_veranstaltung (id {ss_kurs["uni_id"]}) (typ "{mod_ver["type"]}")  (titel '
                                        f'"{ss_kurs["name"].replace("'", "")}"))\n')
                        text_file.write(f'(instance-of (echte_veranstaltung {ss_kurs["uni_id"]}) ('
                                        f'theorie_veranstaltung {mod_ver["uni_id"]}) (semester ss))\n')
