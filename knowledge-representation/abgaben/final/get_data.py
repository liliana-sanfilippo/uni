import json
from api_helpers import get_json_cached


folder = "data/"

API_BASE = "https://ekvv.uni-bielefeld.de/bisapi/v2/"

def get_and_clean_module_data(modul_id, programs):

    try:
        link = API_BASE + f'sinfo/modulDetailsById/{modul_id}'
        json_data = get_json_cached(link)
        if json_data is None:
            print(f"  Keine Moduldaten fuer {modul_id} (uebersprungen)")
            return None
        print(json_data["modul"]["name"])
        modul = json_data["modul"]
        kontexte = json_data["kontexte"]

        new_module_json = {}

        new_module_json["name"] = modul["name"]
        new_module_json["kuerzel"] = modul["kuerzel"]
        new_module_json["lp"] = modul["leistungspunkte"]
        new_module_json["struktur"] = modul["modulstrukturangabe"]
        new_module_json["dauer"] = int(kontexte[0]["dauer"][0])
        new_module_json["programs"] = programs

        # erstmal alle Veranstaltungen in eine Liste werfen
        modell_veranstaltungen = []
        for item in modul["veranstaltungen"]:
            modell_veranstaltungen.append({
                "name": item["name"],
                "type": item["artenAsText"],
                "uni_id": item["id"],
            })

        # Dann die Leistungen durchgehen
        for item in modul["leistungen"]:
            # wenn es eine SL ist, dann den typ sl verwenden
            if item["studienleistung"]:
                typ = "sl"
            # Ansonsten muss es eine Prüfung sein
            else:
                typ = "pr"

            info = {
                "name": item["name"],
                "type": typ,
                "uni_id": item["id"],
            }
            #print(json_data["modul"]["name"])
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
            for mod in modell_veranstaltungen:
                mod["kurse"] = {
                    "ws": [],
                    "ss": []
                }

                for sem in [20261, 20262]:
                    try:
                        link = API_BASE + f'vst/bySemesterAndModellveranstaltung/{sem}/{mod["uni_id"]}'
                        print(link)
                        data = get_json_cached(link)
                        for kurs in data:
                            info = {
                                "name": kurs["thema_kurz"],
                                "uni_id": kurs["vst_id"],
                                "typ": kurs["art"],
                               # "termine": kurs["zeitOrt"],
                                "beleg_nr": kurs["beleg_nr"],
                                "kurztitel": kurs["kurztitel"],
                                "english": kurs["spracheEnglisch"]
                            }
                            if sem == 20261:
                                mod["kurse"]["ws"].append(info)
                            else:
                                mod["kurse"]["ss"].append(info)

                    except Exception as e:
                        print(f"Fehler bei {mod['name']}: {e}")

            new_module_json["veranstaltungen"] = modell_veranstaltungen

        return new_module_json

    except Exception as e:
        print(f"Fehler bei {modul_id}: {e}")




iisy_module = [
    544093118, 543982456, 544074581, 420168424, 544082149, 420164915, 420164915
]

nwi_module = [
    544404773, 544404997
]

complete_json = []

for nr in iisy_module:
    complete_json.append(get_and_clean_module_data(nr, ["IISY"]))

for nr in nwi_module:
    complete_json.append(get_and_clean_module_data(nr, ["NWI"]))


with open("all_data.json", "w") as file:
    json.dump(complete_json, file, indent=2)
