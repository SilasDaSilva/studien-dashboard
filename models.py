class Pruefungsleistung:
    def __init__(self, versuch, note):
        self.versuch = versuch
        self.note = note

    def ist_bestanden(self):
        return self.note <= 4.0

    def als_dict(self):
        return {
            "versuch": self.versuch,
            "note": self.note
        }


class Modul:
    def __init__(self, name, ects, typ="Pflichtmodul", modul_id=None):
        self.modul_id = modul_id
        self.name = name
        self.ects = ects
        self.typ = typ
        self.pruefungen = []

    def beste_note(self):
        if len(self.pruefungen) == 0:
            return None

        beste = self.pruefungen[0].note
        for pruefung in self.pruefungen:
            if pruefung.note < beste:
                beste = pruefung.note
        return beste

    def ist_bestanden(self):
        for pruefung in self.pruefungen:
            if pruefung.ist_bestanden():
                return True
        return False

    def erreichte_ects(self):
        if self.ist_bestanden():
            return self.ects
        return 0

    def status(self):
        if self.ist_bestanden():
            return "bestanden"
        if len(self.pruefungen) > 0:
            return "nicht bestanden"
        return "offen"

    def zeige_info(self):
        note = self.beste_note()
        if note is None:
            note_text = "-"
        else:
            note_text = str(note)

        return self.name + " | " + self.typ + " | " + str(self.ects) + " ECTS | Note: " + note_text + " | " + self.status()

    def als_dict(self):
        pruefungen_liste = []
        for pruefung in self.pruefungen:
            pruefungen_liste.append(pruefung.als_dict())

        return {
            "modul_id": self.modul_id,
            "name": self.name,
            "ects": self.ects,
            "typ": self.typ,
            "pruefungen": pruefungen_liste
        }


class Pflichtmodul(Modul):
    def __init__(self, name, ects, modul_id=None):
        super().__init__(name, ects, "Pflichtmodul", modul_id)


class Wahlpflichtmodul(Modul):
    def __init__(self, name, ects, modul_id=None):
        super().__init__(name, ects, "Wahlpflichtmodul", modul_id)


class Semester:
    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    def modul_hinzufuegen(self, modul):
        self.module.append(modul)

    def erreichte_ects(self):
        summe = 0
        for modul in self.module:
            summe = summe + modul.erreichte_ects()
        return summe

    def durchschnitt(self):
        summe = 0
        ects_summe = 0
        for modul in self.module:
            if modul.ist_bestanden():
                summe = summe + modul.beste_note() * modul.ects
                ects_summe = ects_summe + modul.ects

        if ects_summe == 0:
            return None

        return summe / ects_summe

    def als_dict(self):
        module_liste = []
        for modul in self.module:
            module_liste.append(modul.als_dict())

        return {
            "nummer": self.nummer,
            "module": module_liste
        }


class Studiengang:
    def __init__(self, name, ziel_ects):
        self.name = name
        self.ziel_ects = ziel_ects
        self.student_name = "Silas Ferreira da Silva"
        self.matrikelnummer = "IU14151396"
        self.aktuelles_semester = 1
        self.zieldatum = "01.01.2028"
        self.semester = []

    def semester_finden(self, nummer):
        for sem in self.semester:
            if sem.nummer == nummer:
                return sem
        return None

    def semester_holen_oder_erstellen(self, nummer):
        sem = self.semester_finden(nummer)
        if sem is None:
            sem = Semester(nummer)
            self.semester.append(sem)
        return sem

    def alle_module(self):
        module = []
        for sem in self.semester:
            for modul in sem.module:
                module.append(modul)
        return module

    def alle_module_mit_semester(self):
        module = []
        for sem in self.semester:
            for modul in sem.module:
                module.append([sem.nummer, modul])
        return module

    def modul_nach_nummer(self, nummer):
        module = self.alle_module()
        if nummer < 1 or nummer > len(module):
            return None
        return module[nummer - 1]

    def naechste_modul_id(self):
        groesste_id = 0
        for modul in self.alle_module():
            if modul.modul_id is not None and modul.modul_id > groesste_id:
                groesste_id = modul.modul_id
        return groesste_id + 1

    def modul_finden(self, name):
        for modul in self.alle_module():
            if modul.name.lower() == name.lower():
                return modul
        return None

    def erreichte_ects(self):
        summe = 0
        for modul in self.alle_module():
            summe = summe + modul.erreichte_ects()
        return summe

    def fortschritt_prozent(self):
        if self.ziel_ects == 0:
            return 0
        return self.erreichte_ects() / self.ziel_ects * 100

    def durchschnitt(self):
        summe = 0
        ects_summe = 0
        for modul in self.alle_module():
            if modul.ist_bestanden():
                summe = summe + modul.beste_note() * modul.ects
                ects_summe = ects_summe + modul.ects

        if ects_summe == 0:
            return None

        return summe / ects_summe

    def offene_module(self):
        offene = []
        for modul in self.alle_module():
            if not modul.ist_bestanden():
                offene.append(modul)
        return offene

    def bestandene_module(self):
        bestandene = []
        for modul in self.alle_module():
            if modul.ist_bestanden():
                bestandene.append(modul)
        return bestandene

    def als_dict(self):
        semester_liste = []
        for sem in self.semester:
            semester_liste.append(sem.als_dict())

        return {
            "name": self.name,
            "ziel_ects": self.ziel_ects,
            "student_name": self.student_name,
            "matrikelnummer": self.matrikelnummer,
            "aktuelles_semester": self.aktuelles_semester,
            "zieldatum": self.zieldatum,
            "semester": semester_liste
        }
