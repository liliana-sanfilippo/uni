(deftemplate student (slot id))

(deftemplate modul (slot id) (slot lp) (slot dauer) (slot pr) (slot sl))
(deftemplate in-program (slot modul) (slot programm))
(deftemplate voraussetzung (slot modul) (slot benoetigt))
(deftemplate gehoert-zu-modul (slot echte_veranstaltung) (slot modul))
(deftemplate modul-abgeschlossen (slot student) (slot modul))


(deftemplate theorie_veranstaltung (slot id) (slot modul) (slot typ))
(deftemplate hat-pr (slot theorie_veranstaltung))
(deftemplate hat-sl (slot theorie_veranstaltung))

(deftemplate echte_veranstaltung (slot id) (slot typ) (slot titel))
(deftemplate instance-of (slot echte_veranstaltung) (slot theorie_veranstaltung) (slot semester))

(deftemplate echte_veranstaltung_abgeschlossen (slot student) (slot echte_veranstaltung))
(deftemplate best-pr    (slot student) (slot echte_veranstaltung))
(deftemplate best-sl    (slot student) (slot echte_veranstaltung))

(deftemplate erfuellt-pr (slot student) (slot theorie_veranstaltung))
(deftemplate erfuellt-sl (slot student) (slot theorie_veranstaltung))


(deftemplate frage-waehlbar (slot student) (slot programm) (slot semester))
(deftemplate frage-modul (slot student) (slot modul))
(deftemplate frage-belegen (slot student) (slot echte_veranstaltung) (slot modul))
(deftemplate frage-belegen-sem (slot student) (slot echte_veranstaltung) (slot semester))
(deftemplate frage-belegbar-modul (slot student) (slot modul))
(deftemplate frage-abschluss-sem (slot modul) (slot semester))

(deftemplate kann-belegen (slot student) (slot echte_veranstaltung) (slot modul))
(deftemplate kann-belegen-sem (slot student) (slot echte_veranstaltung) (slot semester))
(deftemplate modul-belegbar (slot student) (slot modul))
(deftemplate fehlende-voraussetzung (slot student) (slot modul) (slot benoetigt))
(deftemplate modul-abschliessbar-sem (slot modul) (slot semester))

(defrule lift-pr
   (best-pr (student ?s) (echte_veranstaltung ?k))
   (instance-of (echte_veranstaltung ?k) (theorie_veranstaltung ?v) (semester ?sem))
   (hat-pr (theorie_veranstaltung ?v))
=> (assert (erfuellt-pr (student ?s) (theorie_veranstaltung ?v))))

(defrule lift-sl
   (best-sl (student ?s) (echte_veranstaltung ?k))
   (instance-of (echte_veranstaltung ?k) (theorie_veranstaltung ?v) (semester ?sem))
   (hat-sl (theorie_veranstaltung ?v))
=> (assert (erfuellt-sl (student ?s) (theorie_veranstaltung ?v))))

(defrule pr-impliziert-abgeschlossen
   (declare (salience 20))
   (best-pr (student ?s) (echte_veranstaltung ?e))
   (not (echte_veranstaltung_abgeschlossen (student ?s) (echte_veranstaltung ?e)))
=> (assert (echte_veranstaltung_abgeschlossen (student ?s) (echte_veranstaltung ?e))))

(defrule ableiten-gehoert-zu-modul
   (declare (salience 20))
   (instance-of (echte_veranstaltung ?e) (theorie_veranstaltung ?t) (semester ?sem))
   (theorie_veranstaltung (id ?t) (modul ?m))
   (not (gehoert-zu-modul (echte_veranstaltung ?e) (modul ?m)))
=> (assert (gehoert-zu-modul (echte_veranstaltung ?e) (modul ?m))))

(defrule ableiten-modul-abgeschlossen
   (declare (salience 10))
   (student (id ?s))
   (modul (id ?m) (pr ?npr) (sl ?nsl))
   (not (modul-abgeschlossen (student ?s) (modul ?m)))
=>
   (bind ?dpr (find-all-facts ((?t theorie_veranstaltung))
      (and (eq ?t:modul ?m)
           (any-factp ((?e erfuellt-pr))
              (and (eq ?e:student ?s) (eq ?e:theorie_veranstaltung ?t:id))))))
   (bind ?dsl (find-all-facts ((?t theorie_veranstaltung))
      (and (eq ?t:modul ?m)
           (any-factp ((?e erfuellt-sl))
              (and (eq ?e:student ?s) (eq ?e:theorie_veranstaltung ?t:id))))))
   (if (and (>= (length$ ?dpr) ?npr) (>= (length$ ?dsl) ?nsl))
      then (assert (modul-abgeschlossen (student ?s) (modul ?m)))))

(defrule ableiten-modul-belegbar
   (declare (salience 5))
   (frage-belegbar-modul (student ?s) (modul ?m))
   (modul (id ?m))
   (not (and (voraussetzung (modul ?m) (benoetigt ?vor))
             (not (modul-abgeschlossen (student ?s) (modul ?vor)))))
=> (assert (modul-belegbar (student ?s) (modul ?m))))

(defrule ableiten-fehlende-voraussetzung
   (declare (salience 5))
   (frage-belegbar-modul (student ?s) (modul ?m))
   (voraussetzung (modul ?m) (benoetigt ?vor))
   (not (modul-abgeschlossen (student ?s) (modul ?vor)))
=> (assert (fehlende-voraussetzung (student ?s) (modul ?m) (benoetigt ?vor))))

(defrule kann-belegen-fuer-modul
   (frage-belegen (student ?s) (echte_veranstaltung ?e) (modul ?m))
   (gehoert-zu-modul (echte_veranstaltung ?e) (modul ?m))
   (not (echte_veranstaltung_abgeschlossen (student ?s) (echte_veranstaltung ?e)))
=> (assert (kann-belegen (student ?s) (echte_veranstaltung ?e) (modul ?m))))

(defrule kann-belegen-im-semester
   (frage-belegen-sem (student ?s) (echte_veranstaltung ?e) (semester ?sem))
   (instance-of (echte_veranstaltung ?e) (theorie_veranstaltung ?t) (semester ?sem))
   (not (echte_veranstaltung_abgeschlossen (student ?s) (echte_veranstaltung ?e)))
=> (assert (kann-belegen-sem (student ?s) (echte_veranstaltung ?e) (semester ?sem))))

(defrule modul-abschliessbar-im-semester
   (frage-abschluss-sem (modul ?m) (semester ?sem))
   (modul (id ?m) (pr ?npr) (sl ?nsl))
=>
   (bind ?apr (find-all-facts ((?t theorie_veranstaltung))
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

