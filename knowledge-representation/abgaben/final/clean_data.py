import json

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
            print("nein")




    new_json["veranstaltungen"] = modell_veranstaltungen

    with open(new_json["kuerzel"]+".json", "w") as file:
        json.dump(new_json, file, indent=2)


# clean_module_data("39-M-Inf-AI-adv-foc_response_1786033745128.json")

clean_module_data("39-M-Inf-AI-adv_a_response_1786033717714.json")


