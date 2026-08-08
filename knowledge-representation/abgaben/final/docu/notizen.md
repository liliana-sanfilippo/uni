# Tech and technology

## Environment and packages

```
 conda create --name kr-env
 
 conda activate kr-env
 
 conda install pip
 conda install python=3.12
 pip install clipspy
 
 (python3 get_data.py)
 (python3 make_facts.py)
 python3 clips_main.py
 
 (python3 test.py)
```

## Web Sources

- https://pypi.org/project/clipspy/
- https://clipspy.readthedocs.io/en/latest/
- https://www.geeksforgeeks.org/python/how-to-remove-key-value-pair-from-a-json-file-in-python/

## Data

- https://ekvv.uni-bielefeld.de/bisapi/openapi/

## API "workflow"

1. get all fsb data via `/vst/bySemesterAndModellveranstaltung/{semester}/{modellveranstaltung_id}`
2. Look for ID of [program]
3. Look for the e1 layer of [program] at `/sinfo/e1ByFsbId/{id}`
4. Look for the e2 layers at `/sinfo/e2ByE1Id/{id}`
5. Get the modules from the e2 layer `/sinfo/e2/{id}`
6. Get the module details `/sinfo/modulDetailsById/{id}`
7. Look for the ID of a Veranstaltung (Modellveranstaltung)
8. Look for current veranstaltungen for this modellveranstaltung
   `/vst/bySemesterAndModellveranstaltung/{semester}/{modellveranstaltung_id}`

### Example program, modules and courses

- **IISY**
    - _FsB ID:_ 366747895
    - _E1 Data Layer:_ 366747897
    - _E2 Layers:_
        * "-": 366747900 (platzhalter?)
            * 39-M-Inf-INT-adv_a: 544093118
            * 39-M-Inf-INT-adv-foc: 543982456
            * 39-M-Inf-INT-app-foc_a: 544074581
            * 39-M-Inf-INT-app: 420168424
            * 39-M-Inf-AI-bas: 420160864
            * 39-M-Inf-AI-adv_a: 544082149
            * 39-M-Inf-AI-adv-foc: 420164915
            * 39-M-Inf-AI-app: 420164915
        * "Modularisierter individueller Kompetenz-Erwerb (MiKE)": 366747902
- **NWI MA**
    - _FSB ID:_ 462589658
    - _E1 data layer:_ 462589642
    - _E2 Layers_:
        * "-": 462589677 (platzhalter?)
            * 39-M-Inf-AI: 544404773
            * 39-M-Inf-AI-x: 544404997
        * "Modularisierter individueller Kompetenz-Erwerb (MiKE)": 462589681

## Beispiele

### Basic example

1. DESCRIPTION
    1. Does the course KURS belong to the module MODULE?
    2. Can I choose the course KURS for the module MODULE?
    3. Is the course KURS available in the SEM semester?
    4. Can I do the module MODULE or am I missing prerequisites?
    5. Can I complete the module MODULE in one SEM semester?
    6. Have I completed the module MODULE?


1. It is (the start of) the winter semester. The student has not completed any courses yet. They want to take the
   module 39-M-Inf-INT-adv_a and want to have the following questions answered:
    1. Does the course "Neural Networks Natural Language Processing" (624620553) belong to the module
       39-M-Inf-INT-adv_a?
    2. Can I choose the course "Neural Networks Natural Language Processing" (624620553) for the module
       39-M-Inf-INT-adv_a?
    3. Is the course "Neural Networks Natural Language Processing" (624620553) available in the winter semester?
    4. Can I do the module 39-M-Inf-INT-adv_a or am I missing prerequisites?
    5. Can I complete the module 39-M-Inf-INT-adv_a in one winter semester?
    6. Have I completed the module 39-M-Inf-INT-adv_a?
2.

| Configuration                             | 1   | 2   | 3   | 4   | 5   | 6   | 6.1 | 7   | 8   | 9   | 10 |
|-------------------------------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|----|
| course belongs to module                  | YES | YES | YES | YES | -   | -   | YES | YES | YES | YES | -  |
| student can take course for module        | YES |     | YES | YES | -   | -   | YES | -   | -   | -   | -  |
| student can take course in given semester | YES | YES | YES | NO  | -   | YES | YES | -   | -   | -   | -  |
| missing prerequisites                     | 0   | 0   | 0   | 1   | 1   | 2   | 2   | 0   | 0   | 0   | 0  |
| can module be completed in given semester | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES | -  |
| has student completed module              | -   | YES | -   | -   | -   | -   | -   | -   | YES | - * | -  |
| course is available in given semester     | YES | YES | YES | -   | -   | YES | YES | YES | YES | YES | -  |
* But another module is with the course of interest

## TODOs

- [ ] Unterschied belongs to und can use for module noch klar machen

## Aufschlüsselungen regeln

### modul-abschliessbar-im-semester

```
// Benennung
(defrule modul-abschliessbar-im-semester
    // welche Frage dazu gehört
    (frage-abschluss-sem (modul ?m) (semester ?sem))
    (modul (id ?m) (pr ?npr) (sl ?nsl))
=>  
    // Alle theorie_veranstaltungen
    (bind ?apr (find-all-facts ((?t theorie_veranstaltung))
        // Die zu dem gegebenen Modul gehören
        (and (eq ?t:modul ?m)
            (any-factp ((?h hat-pr)) (eq ?h:theorie_veranstaltung ?t:id))
            (any-factp ((?i instance-of))
                (and (eq ?i:theorie_veranstaltung ?t:id) (eq ?i:semester ?sem))))))
    (bind ?asl (find-all-facts ((?t theorie_veranstaltung))
        (and (eq ?t:modul ?m)
            (any-factp ((?h hat-sl)) (eq ?h:theorie_veranstaltung ?t:id))
            (any-factp ((?i instance-of))
                (and (eq ?i:theorie_veranstaltung ?t:id) (eq ?i:semester ?sem))))))
    (if (and (>= (length$ ?apr) ?npr) (>= (length$ ?asl) ?nsl))
        then (assert (modul-abschliessbar-sem (modul ?m) (semester ?sem)))))
```

### ableiten-modul-abgeschlossen

```
(defrule ableiten-modul-abgeschlossen
   (declare (salience 10))
   (student (id ?s))
   (modul (id ?m) (pr ?npr) (sl ?nsl))
   (not (modul-abgeschlossen (student ?s) (modul ?m)))
=>
   // Alle theorie_veranstaltungen finden 
   (bind ?dpr (find-all-facts ((?t theorie_veranstaltung))
      // Die zu dem gegebenen Modul gehören
      (and (eq ?t:modul ?m)
           // und suche alle erfuellt-pr facts heraus
           (any-factp ((?e erfuellt-pr))
              // Schaue dann, ob der Student eine theorie_veranstaltung des moduls abgeschlossen hat 
              (and (eq ?e:student ?s) (eq ?e:theorie_veranstaltung ?t:id))))))
   (bind ?dsl (find-all-facts ((?t theorie_veranstaltung))
      (and (eq ?t:modul ?m)
           (any-factp ((?e erfuellt-sl))
              (and (eq ?e:student ?s) (eq ?e:theorie_veranstaltung ?t:id))))))
   (if (and (>= (length$ ?dpr) ?npr) (>= (length$ ?dsl) ?nsl))
      then (assert (modul-abgeschlossen (student ?s) (modul ?m)))))
```
