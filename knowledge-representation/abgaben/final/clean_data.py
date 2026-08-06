import json
import requests

folder = "data/"

API_BASE = "https://ekvv.uni-bielefeld.de/bisapi/v2/"

def clean_module_data(filename):
    with open(folder+filename, 'r') as file:
        json_data = json.load(file)

    modul = json_data["modul"]
    kontexte = json_data["kontexte"]

    new_json = {}

    new_json["name"] = modul["name"]
    new_json["kuerzel"] = modul["kuerzel"]
    new_json["lp"] = modul["leistungspunkte"]
    new_json["struktur"] = modul["modulstrukturangabe"]
    new_json["dauer"] = int(kontexte[0]["dauer"][0])

    modell_veranstaltungen = []
    for item in modul["veranstaltungen"]:
        modell_veranstaltungen.append({
            "name": item["name"],
            "type": item["artenAsText"],
            "uni_id": item["id"],
        })

    for item in modul["leistungen"]:
        if item["studienleistung"]:
            typ = "sl"
        else:
            typ = "pr"

        info = {
            "name": item["name"],
            "type": typ,
            "uni_id": item["id"],
        }

        if "veranstaltung" in item:
            for ver in modell_veranstaltungen:
                if ver["uni_id"] == item["veranstaltung"]:
                    if "leistungen" in ver:
                        ver["leistungen"].append(info)
                    else:
                        ver["leistungen"] = [info]
        else:
            for ver in modell_veranstaltungen:
                if ver["type"] == "Seminar" or ver["type"] == "Vorlesung":
                    if "leistungen" in ver:
                        ver["leistungen"].append(info)
                    else:
                        ver["leistungen"] = [info]


            # noch Veranstaltungsinfos dazu holen
        for item in modell_veranstaltungen:
            item["kurse"] = {
                "ws": [],
                "ss": []
            }
            for sem in [20261, 20262]:
                try:
                    link = API_BASE + f'vst/bySemesterAndModellveranstaltung/{sem}/{item["uni_id"]}'
                    print(link)
                    response = requests.get(link)
                    data = response.json()
                    for kurs in data:
                        info = {
                            "name": kurs["thema_kurz"],
                            "uni_id": kurs["vst_id"],
                            "typ": kurs["art"],
                            "termine": kurs["zeitOrt"],
                            "beleg_nr": kurs["beleg_nr"],
                            "kurztitel": kurs["kurztitel"],
                            "english": kurs["spracheEnglisch"]
                        }
                    if sem == 20261:
                        item["kurse"]["ws"].append(info)
                    else:
                        item["kurse"]["ss"].append(info)

                except Exception as e:
                    print(f"Fehler bei Team {item['name']}: {e}")

    new_json["veranstaltungen"] = modell_veranstaltungen

    with open(new_json["kuerzel"]+".json", "w") as file:
        json.dump(new_json, file, indent=2)


clean_module_data("39-M-Inf-AI-adv-foc_response_1786033745128.json")

clean_module_data("39-M-Inf-AI-adv_a_response_1786033717714.json")


