# Tech and technology

## Environment and packages

```
 conda create --name kr-env
 
 conda activate kr-env
 
 conda install pip
 conda install python=3.12
 pip install clipspy
 
 python3 get_data.py
 python3 make_facts.py
 python3 main.py
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

1. Student wants to check 

| Configuration            | 1                                                    | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|--------------------------|------------------------------------------------------|---|---|---|---|---|---|---|---|----|
| Relevant modules         | 39-M-Inf-INT-adv_a                                   |   |   |   |   |   |   |   |   |    |
| Relevant courses         | Advanced Interaction Technology: Seminar (659886362) |   |   |   |   |   |   |   |   |    |
| Prequisites              | None                                                 |   |   |   |   |   |   |   |   |    |
| Course offers            | In the current semester                              |   |   |   |   |   |   |   |   |    |
| Course belongs to module | Yes                                                  |   |   |   |   |   |   |   |   |    |
| Course completion        | No courses completed yet                             |   |   |   |   |   |   |   |   |    |


