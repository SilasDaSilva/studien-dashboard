from models import Pruefungsleistung, Pflichtmodul, Wahlpflichtmodul


class NotenManager:
    def __init__(self, repository):
        self.repository = repository
        self.studiengang = repository.laden()

    def modul_hinzufuegen(self, name, ects, semester_nummer, typ):
        if self.studiengang.modul_finden(name) is not None:
            return False

        semester = self.studiengang.semester_holen_oder_erstellen(semester_nummer)
        modul_id = self.studiengang.naechste_modul_id()
        if typ == "Pflichtmodul":
            modul = Pflichtmodul(name, ects, modul_id)
        else:
            modul = Wahlpflichtmodul(name, ects, modul_id)
        semester.modul_hinzufuegen(modul)
        return True

    def note_eintragen(self, modul_name, note):
        modul = self.studiengang.modul_finden(modul_name)
        if modul is None:
            return False
        if modul.ist_bestanden():
            return "bestanden"

        versuch = len(modul.pruefungen) + 1
        pruefung = Pruefungsleistung(versuch, note)
        modul.pruefungen.append(pruefung)
        return True

    def note_eintragen_nach_nummer(self, nummer, note):
        modul = self.studiengang.modul_nach_nummer(nummer)
        if modul is None:
            return False
        if modul.ist_bestanden():
            return "bestanden"

        versuch = len(modul.pruefungen) + 1
        pruefung = Pruefungsleistung(versuch, note)
        modul.pruefungen.append(pruefung)
        return True

    def modul_loeschen(self, nummer):
        modul = self.studiengang.modul_nach_nummer(nummer)
        if modul is None:
            return False

        for semester in self.studiengang.semester:
            if modul in semester.module:
                semester.module.remove(modul)
                return True
        return False

    def speichern(self):
        self.repository.speichern(self.studiengang)

    def aktuelles_semester_setzen(self, semester):
        self.studiengang.aktuelles_semester = semester
