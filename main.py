import datetime
from manager import NotenManager
from storage import JsonRepository


def eingabe_text(frage):
    while True:
        wert = input(frage).strip()
        if wert != "":
            return wert
        print("Bitte etwas eingeben.")


def eingabe_int(frage):
    while True:
        text = input(frage).strip()
        try:
            zahl = int(text)
            if zahl > 0:
                return zahl
            print("Bitte eine Zahl groesser als 0 eingeben.")
        except ValueError:
            print("Bitte eine ganze Zahl eingeben.")


def eingabe_float(frage):
    while True:
        text = input(frage).strip()
        text = text.replace(",", ".")
        try:
            zahl = float(text)
            if zahl >= 1.0 and zahl <= 5.0:
                return zahl
            print("Bitte eine Note zwischen 1.0 und 5.0 eingeben.")
        except ValueError:
            print("Bitte eine Zahl eingeben, zum Beispiel 2.0 oder 2,0.")


def eingabe_modultyp():
    while True:
        print("Typ auswaehlen:")
        print("1 - Pflichtmodul")
        print("2 - Wahlpflichtmodul")
        auswahl = input("Auswahl: ").strip()
        if auswahl == "1" or auswahl == "":
            return "Pflichtmodul"
        if auswahl == "2":
            return "Wahlpflichtmodul"
        print("Bitte 1 oder 2 eingeben.")


def eingabe_datum(frage):
    while True:
        text = input(frage).strip()
        try:
            teile = text.split(".")
            tag = int(teile[0])
            monat = int(teile[1])
            jahr = int(teile[2])
            datetime.date(jahr, monat, tag)
            return text
        except:
            print("Bitte ein gueltiges Datum eingeben, zum Beispiel 01.01.2028.")


def zieldatum_als_date(zieldatum_str):
    try:
        teile = zieldatum_str.split(".")
        tag = int(teile[0])
        monat = int(teile[1])
        jahr = int(teile[2])
        return datetime.date(jahr, monat, tag)
    except:
        return None


def countdown_berechnen(zieldatum_str):
    ziel = zieldatum_als_date(zieldatum_str)
    if ziel is None:
        return "unbekannt"
    heute = datetime.date.today()
    tage = (ziel - heute).days
    if tage < 0:
        return str(abs(tage)) + " Tage ueberfaellig"
    return str(tage) + " Tage"


def fortschrittsbalken(erreicht, gesamt, breite=20):
    if gesamt == 0:
        return "[" + "." * breite + "]"
    gefuellt = int(erreicht / gesamt * breite)
    if gefuellt > breite:
        gefuellt = breite
    return "[" + "|" * gefuellt + "." * (breite - gefuellt) + "]"


def ampel_berechnen(studiengang):
    ziel = zieldatum_als_date(studiengang.zieldatum)
    if ziel is None:
        return "?"

    heute = datetime.date.today()
    verbleibende_tage = (ziel - heute).days

    if verbleibende_tage <= 0:
        return "ROT"

    verbleibende_ects = studiengang.ziel_ects - studiengang.erreichte_ects()

    if verbleibende_ects <= 0:
        return "GRUEN"

    verbleibende_monate = verbleibende_tage / 30.5
    benoetigt_pro_monat = verbleibende_ects / verbleibende_monate

    if benoetigt_pro_monat <= 5:
        return "GRUEN"
    elif benoetigt_pro_monat <= 8:
        return "GELB"
    else:
        return "ROT"


def ampel_als_text(ampel):
    if ampel == "GRUEN":
        return "Im Zeitplan"
    elif ampel == "GELB":
        return "Aufholen!"
    else:
        return "In Gefahr!"


def note_text(modul):
    note = modul.beste_note()
    if note is None:
        return "-"
    return str(note)


def zeige_modul_zeile(nummer, semester, modul):
    text = str(nummer) + ". "
    text = text + "Sem. " + str(semester) + " | "
    text = text + modul.name + " | "
    text = text + modul.typ + " | "
    text = text + str(modul.ects) + " ECTS | "
    text = text + "Note: " + note_text(modul) + " | "
    text = text + "Versuche: " + str(len(modul.pruefungen)) + " | "
    text = text + modul.status()
    print(text)


def zeige_alle_module(manager):
    module = manager.studiengang.alle_module_mit_semester()
    print()
    print("==== Alle Faecher ====")
    if len(module) == 0:
        print("Noch keine Faecher gespeichert.")
    else:
        nummer = 1
        for eintrag in module:
            zeige_modul_zeile(nummer, eintrag[0], eintrag[1])
            nummer = nummer + 1
    print()


def zeige_module(titel, module):
    print()
    print("==== " + titel + " ====")
    if len(module) == 0:
        print("Keine Module gefunden.")
    else:
        for modul in module:
            print(modul.zeige_info())
    print()


def zeige_dashboard(manager):
    studiengang = manager.studiengang
    heute = datetime.date.today()
    jetzt = datetime.datetime.now()

    ampel = ampel_berechnen(studiengang)
    countdown = countdown_berechnen(studiengang.zieldatum)
    balken = fortschrittsbalken(studiengang.erreichte_ects(), studiengang.ziel_ects)
    ects_text = str(studiengang.erreichte_ects()) + " / " + str(studiengang.ziel_ects) + " ECTS"

    durchschnitt = studiengang.durchschnitt()
    if durchschnitt is None:
        note_anzeige = "noch keine"
    else:
        note_anzeige = str(round(durchschnitt, 2))

    print()
    print("=" * 60)
    print("  Study Progress Tracker")
    print("=" * 60)
    print("  Student:    " + studiengang.student_name)
    print("  Matrikel:   " + studiengang.matrikelnummer)
    print("  Semester:   " + str(studiengang.aktuelles_semester))
    print("  Datum:      " + heute.strftime("%d.%m.%Y") + "   Uhrzeit: " + jetzt.strftime("%H:%M"))
    print("  Zieldatum:  " + studiengang.zieldatum + "   Countdown: " + countdown)
    print("-" * 60)
    print()
    print("  FORTSCHRITT         ZEITPLAN          NOTENSCHNITT")
    print("  " + balken + "  [ " + ampel + " ]        [ Ø " + note_anzeige + " ]")
    print("  " + ects_text + "        " + ampel_als_text(ampel) + "           Ziel: < 2.0")
    print()
    print("-" * 60)

    offene = studiengang.offene_module()
    print("  AKTUELLE KURSE (offen)")
    if len(offene) == 0:
        print("  Alle Module bestanden!")
    else:
        for modul in offene:
            print("  - " + modul.name + " | " + modul.typ + " | " + str(modul.ects) + " ECTS | " + modul.status())

    print()
    bestandene = studiengang.bestandene_module()
    print("  BESTANDENE KURSE")
    if len(bestandene) == 0:
        print("  Noch keine Module bestanden.")
    else:
        for modul in bestandene:
            print("  - " + modul.name + " | Note: " + note_text(modul) + " | " + str(modul.ects) + " ECTS")

    print()
    print("=" * 60)
    print()


def modul_hinzufuegen(manager):
    print()
    zeige_alle_module(manager)
    name = eingabe_text("Name des Moduls: ")
    ects = eingabe_int("ECTS: ")
    semester = eingabe_int("Semester: ")
    typ = eingabe_modultyp()

    gespeichert = manager.modul_hinzufuegen(name, ects, semester, typ)
    if gespeichert:
        print("Modul wurde hinzugefuegt.")
    else:
        print("Dieses Modul gibt es schon.")


def modul_loeschen(manager):
    module = manager.studiengang.alle_module()
    if len(module) == 0:
        print()
        print("Es gibt noch keine Module.")
        print()
        return

    zeige_alle_module(manager)
    nummer = eingabe_int("Nummer des Moduls das geloescht werden soll: ")

    geloescht = manager.modul_loeschen(nummer)
    if geloescht:
        print("Modul wurde geloescht.")
    else:
        print("Diese Nummer gibt es nicht.")


def note_eintragen(manager):
    module = manager.studiengang.alle_module()
    if len(module) == 0:
        print()
        print("Es gibt noch keine Module. Bitte erst ein Modul hinzufuegen.")
        print()
        return

    zeige_alle_module(manager)
    nummer = eingabe_int("Nummer des Moduls: ")
    note = eingabe_float("Note: ")

    gefunden = manager.note_eintragen_nach_nummer(nummer, note)
    if gefunden == True:
        print("Note wurde eingetragen.")
    elif gefunden == "bestanden":
        print("Dieses Modul ist schon bestanden. Es wird keine weitere Note eingetragen.")
    else:
        print("Diese Nummer gibt es nicht.")


def aktuelles_semester_setzen(manager):
    print()
    print("Aktuelles Semester: " + str(manager.studiengang.aktuelles_semester))
    semester = eingabe_int("Neues Semester: ")
    manager.aktuelles_semester_setzen(semester)
    print("Aktuelles Semester wurde gespeichert.")
    print()


def zieldatum_setzen(manager):
    print()
    print("Aktuelles Zieldatum: " + manager.studiengang.zieldatum)
    datum = eingabe_datum("Neues Zieldatum (z.B. 01.01.2028): ")
    manager.studiengang.zieldatum = datum
    print("Zieldatum wurde gespeichert.")
    print()


def zeige_menue():
    print("1 - Dashboard anzeigen")
    print("2 - Modul hinzufuegen")
    print("3 - Modul loeschen")
    print("4 - Note eintragen")
    print("5 - Offene Module anzeigen")
    print("6 - Bestandene Module anzeigen")
    print("7 - Aktuelles Semester festlegen")
    print("8 - Zieldatum aendern")
    print("9 - Speichern")
    print("0 - Beenden")


def main():
    repository = JsonRepository("data.json")
    manager = NotenManager(repository)

    while True:
        zeige_menue()
        auswahl = input("Auswahl: ")

        if auswahl == "1":
            zeige_dashboard(manager)
        elif auswahl == "2":
            modul_hinzufuegen(manager)
        elif auswahl == "3":
            modul_loeschen(manager)
        elif auswahl == "4":
            note_eintragen(manager)
        elif auswahl == "5":
            zeige_module("Offene / nicht bestandene Module", manager.studiengang.offene_module())
        elif auswahl == "6":
            zeige_module("Bestandene Module", manager.studiengang.bestandene_module())
        elif auswahl == "7":
            aktuelles_semester_setzen(manager)
        elif auswahl == "8":
            zieldatum_setzen(manager)
        elif auswahl == "9":
            manager.speichern()
            print("Daten wurden gespeichert.")
        elif auswahl == "0":
            manager.speichern()
            print("Daten wurden gespeichert. Programm beendet.")
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    main()
