import clips
import argparse

parser = argparse.ArgumentParser(description='description')
parser.add_argument('can-take-in-sem')

args = parser.parse_args()

environment = clips.Environment()

environment.load("clip_definitionen.clp")
environment.reset()
with open("fakten.txt", "r") as text_file:
    fakten =  text_file.readlines()

print(len(fakten))

for f in fakten:
    environment.assert_string(f)


with open("mockup_01.txt", "r") as mock01:
    m01 =  mock01.readlines()

for f in m01:
    environment.assert_string(f)



environment.assert_string(
    '(frage-belegen (student liliana) (echte_veranstaltung 544093131) (modul "39-M-Inf-INT-adv_a"))'
)

environment.run()


all_fact_names = []

for fact in environment.facts():
    #print(fact)
    all_fact_names.append(str(fact))

if '(kann-belegen-sem (student liliana) (echte_veranstaltung 659886362) (semester ws))' in all_fact_names:
    print("JA")

