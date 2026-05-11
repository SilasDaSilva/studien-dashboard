import json
import os

from models import Studiengang, Semester, Modul, Pruefungsleistung, Pflichtmodul, Wahlpflichtmodul


class JsonRepository:
    def __init__(self, dateiname, meldungen_anzeigen=True):
        self.dateiname = dateiname
        self.meldungen_anzeigen = meldungen_anzeigen

    def laden(self):
        if not os.path.exists(self.dateiname):
            return Studiengang("Angewandte KI", 180)

        try:
            datei = open(self.dateiname, "r", encoding="utf-8")
            daten = json.load(datei)
            datei.close()
        except:
            if self.meldungen_anzeigen:
                print("Speicherdatei ist fehlerhaft. Es werden leere Daten gestartet.")
            return Studiengang("Angewandte KI", 180)

        studiengang = Studiengang(daten["name"], daten["ziel_ects"])
        studiengang.student_name = daten.get("student_name", "Silas Ferreira da Silva")
        studiengang.matrikelnummer = daten.get("matrikelnummer", "IU14151396")
        studiengang.aktuelles_semester = daten.get("aktuelles_semester", 1)
        studiengang.zieldatum = daten.get("zieldatum", "01.01.2028")

        for sem_daten in daten["semester"]:
            semester = Semester(sem_daten["nummer"])

            for modul_daten in sem_daten["module"]:
                modul_id = modul_daten.get("modul_id")
                if modul_id is None:
                    modul_id = studiengang.naechste_modul_id()
                if modul_daten["typ"] == "Pflichtmodul":
                    modul = Pflichtmodul(modul_daten["name"], modul_daten["ects"], modul_id)
                else:
                    modul = Wahlpflichtmodul(modul_daten["name"], modul_daten["ects"], modul_id)

                for pruefung_daten in modul_daten["pruefungen"]:
                    pruefung = Pruefungsleistung(pruefung_daten["versuch"], pruefung_daten["note"])
                    modul.pruefungen.append(pruefung)

                semester.module.append(modul)

            studiengang.semester.append(semester)

        return studiengang

    def speichern(self, studiengang):
        datei = open(self.dateiname, "w", encoding="utf-8")
        json.dump(studiengang.als_dict(), datei, indent=4, ensure_ascii=False)
        datei.close()
