(deftemplate modul          (slot id) (slot lp) (slot dauer))
(deftemplate modell_veranstaltung  (slot id) (slot modul) (slot typ))
(deftemplate veranstaltung           (slot id) (slot typ) (slot titel))
(deftemplate angeboten      (slot modell_veranstaltung) (slot veranstaltung) (slot semester))
(deftemplate in-program     (slot modul) (slot programm))
(deftemplate abgeschlossen  (slot student) (slot modell_veranstaltung))


(deftemplate braucht        (slot modul) (slot modell_veranstaltung))
(deftemplate braucht-gruppe (slot modul) (slot gruppe))
(deftemplate gruppe-option  (slot gruppe) (slot modell_veranstaltung))


(deftemplate frage-waehlbar (slot student) (slot programm) (slot semester))
(deftemplate frage-modul    (slot student) (slot modul))


(deftemplate waehlbar       (slot student) (slot veranstaltung) (slot programm) (slot semester))
(deftemplate modul-erfuellt (slot student) (slot modul))


(defrule r-veranstaltung-waehlbar
   (frage-waehlbar (student ?s) (programm ?p) (semester ?sem))
   (angeboten (modell_veranstaltung ?v) (veranstaltung ?k) (semester ?sem))
   (modell_veranstaltung (id ?v) (modul ?m))
   (in-program (modul ?m) (programm ?p))
   (not (abgeschlossen (student ?s) (modell_veranstaltung ?v)))
=>
   (assert (waehlbar (student ?s) (veranstaltung ?k) (programm ?p) (semester ?sem))))


(defrule r-modul-erfuellt
   (frage-modul (student ?s) (modul ?m))
   (modul (id ?m))
   (not (and (braucht (modul ?m) (modell_veranstaltung ?v))
             (not (abgeschlossen (student ?s) (modell_veranstaltung ?v)))))
   (not (and (braucht-gruppe (modul ?m) (gruppe ?g))
             (not (and (gruppe-option (gruppe ?g) (modell_veranstaltung ?vo))
                       (abgeschlossen (student ?s) (modell_veranstaltung ?vo))))))
=>
   (assert (modul-erfuellt (student ?s) (modul ?m))))