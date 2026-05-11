from models import Modul, Pruefungsleistung, Semester, Studiengang, Pflichtmodul, Wahlpflichtmodul


def test_modul_bestanden():
    modul = Modul("Einfuehrung in die Programmierung mit Python", 5)
    modul.pruefungen.append(Pruefungsleistung(1, 2.0))

    assert modul.ist_bestanden() == True
    assert modul.erreichte_ects() == 5


def test_modul_nicht_bestanden():
    modul = Modul("Mathematik: Analysis", 5)
    modul.pruefungen.append(Pruefungsleistung(1, 5.0))

    assert modul.ist_bestanden() == False
    assert modul.erreichte_ects() == 0


def test_studiengang_fortschritt():
    studiengang = Studiengang("Angewandte KI", 180)
    semester = Semester(1)

    modul1 = Modul("Einfuehrung in die Programmierung mit Python", 5)
    modul1.pruefungen.append(Pruefungsleistung(1, 2.0))

    modul2 = Modul("Mathematik: Analysis", 5)

    semester.module.append(modul1)
    semester.module.append(modul2)
    studiengang.semester.append(semester)

    assert studiengang.erreichte_ects() == 5
    assert round(studiengang.fortschritt_prozent(), 2) == 2.78
    assert studiengang.offene_module()[0].name == "Mathematik: Analysis"


def test_modul_mit_semester_liste():
    studiengang = Studiengang("Angewandte KI", 180)
    semester = Semester(2)
    modul = Modul("Artificial Intelligence", 5)
    semester.module.append(modul)
    studiengang.semester.append(semester)

    liste = studiengang.alle_module_mit_semester()

    assert liste[0][0] == 2
    assert liste[0][1].name == "Artificial Intelligence"


def test_modul_nach_nummer_finden():
    studiengang = Studiengang("Angewandte KI", 180)
    semester = Semester(1)
    semester.module.append(Modul("Einfuehrung in die Programmierung mit Python", 5))
    semester.module.append(Modul("Mathematik: Analysis", 5))
    studiengang.semester.append(semester)

    modul = studiengang.modul_nach_nummer(2)

    assert modul.name == "Mathematik: Analysis"
    assert studiengang.modul_nach_nummer(99) is None


def test_note_fuer_falsche_modulnummer():
    from manager import NotenManager

    class TestRepository:
        def laden(self):
            studiengang = Studiengang("Angewandte KI", 180)
            semester = Semester(1)
            semester.module.append(Modul("Einfuehrung in die Programmierung mit Python", 5))
            studiengang.semester.append(semester)
            return studiengang

        def speichern(self, studiengang):
            pass

    manager = NotenManager(TestRepository())

    assert manager.note_eintragen_nach_nummer(99, 2.0) == False


def test_gewichteter_durchschnitt():
    studiengang = Studiengang("Angewandte KI", 180)
    semester = Semester(1)

    modul1 = Modul("Einfuehrung in die Programmierung mit Python", 5)
    modul1.pruefungen.append(Pruefungsleistung(1, 1.0))

    modul2 = Modul("Projekt: Objektorientierte und funktionale Programmierung mit Python", 10)
    modul2.pruefungen.append(Pruefungsleistung(1, 2.0))

    semester.module.append(modul1)
    semester.module.append(modul2)
    studiengang.semester.append(semester)

    assert round(studiengang.durchschnitt(), 2) == 1.67


def test_status_nicht_bestanden():
    modul = Modul("Mathematik: Analysis", 5)
    assert modul.status() == "offen"

    modul.pruefungen.append(Pruefungsleistung(1, 5.0))
    assert modul.status() == "nicht bestanden"


def test_doppeltes_modul_verhindern():
    from manager import NotenManager

    class TestRepository:
        def laden(self):
            return Studiengang("Angewandte KI", 180)

        def speichern(self, studiengang):
            pass

    manager = NotenManager(TestRepository())

    assert manager.modul_hinzufuegen("Einfuehrung in die Programmierung mit Python", 5, 1, "Pflichtmodul") == True
    assert manager.modul_hinzufuegen("einfuehrung in die programmierung mit python", 5, 1, "Pflichtmodul") == False


def test_keine_note_nach_bestanden():
    from manager import NotenManager

    class TestRepository:
        def laden(self):
            studiengang = Studiengang("Angewandte KI", 180)
            semester = Semester(1)
            modul = Modul("Einfuehrung in die Programmierung mit Python", 5)
            modul.pruefungen.append(Pruefungsleistung(1, 2.0))
            semester.module.append(modul)
            studiengang.semester.append(semester)
            return studiengang

        def speichern(self, studiengang):
            pass

    manager = NotenManager(TestRepository())

    assert manager.note_eintragen_nach_nummer(1, 1.0) == "bestanden"


def test_kaputte_json_startet_leer():
    import os
    import tempfile
    from storage import JsonRepository

    ordner = tempfile.mkdtemp()
    dateiname = os.path.join(ordner, "data.json")
    datei = open(dateiname, "w", encoding="utf-8")
    datei.write("{kaputt")
    datei.close()

    repository = JsonRepository(dateiname, False)
    studiengang = repository.laden()

    assert studiengang.name == "Angewandte KI"
    assert len(studiengang.semester) == 0


def test_aktuelles_semester_setzen():
    from manager import NotenManager

    class TestRepository:
        def laden(self):
            return Studiengang("Angewandte KI", 180)

        def speichern(self, studiengang):
            pass

    manager = NotenManager(TestRepository())
    manager.aktuelles_semester_setzen(3)

    assert manager.studiengang.aktuelles_semester == 3


def test_modul_loeschen():
    from manager import NotenManager

    class TestRepository:
        def laden(self):
            studiengang = Studiengang("Angewandte KI", 180)
            semester = Semester(1)
            semester.module.append(Modul("Einfuehrung in die Programmierung mit Python", 5))
            semester.module.append(Modul("Mathematik: Analysis", 5))
            studiengang.semester.append(semester)
            return studiengang

        def speichern(self, studiengang):
            pass

    manager = NotenManager(TestRepository())

    assert len(manager.studiengang.alle_module()) == 2
    assert manager.modul_loeschen(1) == True
    assert len(manager.studiengang.alle_module()) == 1
    assert manager.studiengang.alle_module()[0].name == "Mathematik: Analysis"
    assert manager.modul_loeschen(99) == False


def test_subklassen():
    pflicht = Pflichtmodul("Einfuehrung in die Programmierung mit Python", 5)
    wahl = Wahlpflichtmodul("Kommunikation im Beruf", 5)

    assert isinstance(pflicht, Pflichtmodul)
    assert isinstance(wahl, Wahlpflichtmodul)
    assert pflicht.typ == "Pflichtmodul"
    assert wahl.typ == "Wahlpflichtmodul"


if __name__ == "__main__":
    test_modul_bestanden()
    test_modul_nicht_bestanden()
    test_studiengang_fortschritt()
    test_modul_mit_semester_liste()
    test_modul_nach_nummer_finden()
    test_note_fuer_falsche_modulnummer()
    test_gewichteter_durchschnitt()
    test_status_nicht_bestanden()
    test_doppeltes_modul_verhindern()
    test_keine_note_nach_bestanden()
    test_kaputte_json_startet_leer()
    test_aktuelles_semester_setzen()
    test_modul_loeschen()
    test_subklassen()
    print("Alle Tests erfolgreich.")
