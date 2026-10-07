import streamlit as st
import socket, os

# Konfiguration für den Mathetag 2026

# Workshopreihen

# kosten[0]: falls man den Erstwunsch bekommt
# kosten[1]: falls man den Zweitwunsch bekommt
# kosten[2]: falls man keinen der beiden Wünschen bekommt

datum = "13.11.2026"

workshopreihe = [
    {
        "name" : "Vormittag",
        "wunschspalten" : ["erstwunschvm", ("zweitwunschvm_{}", "erstwunschvm")],
        "kosten" : [0, 2, 5],
        "data" : [
            {
                "name_kurz" : "ws1",
                "name" : "Workshop 1",
                "titel" : "Die Welt der Fraktale (Eric Trébuchon)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws2",
                "name" : "Workshop 2",
                "titel" : "Die unglaubliche Beweis-Maschine (Prof. Dr. Peter Pfaffelhuber)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws3",
                "name" : "Workshop 3",
                "titel" : "Topologie – ein Papierband ohne Innen und Außen (Dr. Maximilian Stegemeyer)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws4",
                "name" : "Workshop 4",
                "titel" : "A Gödelian Journey to the Island of Knights and Knaves (Dr. Alberto Miguel Gomez)",
                "groesse" : 30
            }
        ]
    },
    {
        "name" : "Nachmittag",
        "wunschspalten" : ["erstwunschnm", ("zweitwunschnm_{}", "erstwunschnm")],
        "kosten" : [0, 2, 5],
        "data" : [
            {
                "name_kurz" : "ws5",
                "name" : "Workshop 5",
                "titel" : "Sieben Fragen, eine Lüge (Dr. Riccardo Tosi)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws6",
                "name" : "Workshop 6",
                "titel" : "Mathe, Mäckes und fleischfressende Pflanzen – und wie krumm sind Bananen? (Dr. Jonathan Brugger)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws7",
                "name" : "Workshop 7",
                "titel" : "Fibonacci und die Folge(n) (Dr. Ernst August v. Hammerstein)",
                "groesse" : 30
            }
        ]
    }
]

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

mail_betreff = "Einteilung für den Mathetag am " + datum

mail_body = """
<p>Hallo {Vorname} {Nachname},</p>

<p>wir freuen uns, dich am Freitag, den {Datum}, zum Mathetag an der Universität
Freiburg begrüßen zu dürfen. Wir starten um 8:45 Uhr im Hörsaal II (1. OG) des Instituts für Geo- und Umweltnaturwissenschaften in der <a href="https://www.openstreetmap.org/?mlat=48.002320&mlon=7.847924#map=19/48.002320/7.847924">Albertstraße 23b</a>. Alle weiteren Infos zum Mathetag – Programm, Ablauf und Wegbeschreibung – findest du auf unserer <a href="https://uni-freiburg.de/mathematik-didaktik/mathematik-tag/">Webseite</a>.</p>

<p>Die Workshops haben wir so zugeteilt, dass möglichst viele ihren Erstwunsch
bekommen. Dir wurden folgende Workshops zugeteilt:</p>

<ul>
<li><b>Vormittag (10:00 – 11:30 Uhr):</b> {EinteilungVormittag}: {WorkshopnameVormittag}</li>
<li><b>Nachmittag (13:00 – 14:30 Uhr):</b> {EinteilungNachmittag}: {WorkshopnameNachmittag}</li>
</ul>

<p>Am Ende der Veranstaltung erhältst du von uns eine Teilnahmebescheinigung,
die du in der Schule vorzeigen kannst.</p>

<p>Falls du doch nicht teilnehmen kannst, schreib uns bitte kurz an <a href="mailto:didaktik@math.uni-freiburg.de">didaktik@math.uni-freiburg.de</a>, damit dein Platz an jemand anderen gehen kann.</p>

<p>Viele Grüße,<br>
Dein Mathetag-Team</p>

<p>Du erhältst diese Mail, weil du dich für den <a href="https://uni-freiburg.de/mathematik-didaktik/mathematik-tag/">Mathetag des
Mathematischen Instituts</a> angemeldet hast. Bei Fragen schreibe bitte direkt
an <a href="mailto:didaktik@math.uni-freiburg.de">uns</a>.</p>

<p>Universität Freiburg<br>
Abteilung Didaktik der Mathematik<br>
Ernst-Zermelo-Str. 1<br>
79104 Freiburg</p>

<img src="https://www.math.uni-freiburg.de/static/images/ufr.png"
     alt="Universität Freiburg" width="300" />
"""

# {Datum} wird hier ersetzt, alle anderen Platzhalter erst in MATHETAG.py
mail_body = mail_body.replace("{Datum}", datum)

workshop_dict = { w["name_kurz"] : w["titel"] for wr in workshopreihe for w in wr["data"] }
workshopname_dict = { w["name_kurz"] : w["name"] for wr in workshopreihe for w in wr["data"] }
workshopsize_dict = { w["name_kurz"] : w["groesse"] for wr in workshopreihe for w in wr["data"] }

for wr in workshopreihe:
    wr["anzahl_wuensche"] = len(wr["wunschspalten"])
    if len(wr["wunschspalten"]) + 1 != len(wr["kosten"]):
        st.error(f"Konfiguration fehlerhaft. In {wr['name']} ist eine falsche Anzahl von Kosten angegeben. (Muss eins mehr als die Anzahl der Wunschspalten sein.)") 

# Spaltennamen im REDCap-Export (Variablennamen aus edition_2026/redcap_datadictionary2026.csv)
#
# Ein Eintrag in "wunschspalten" ist entweder
#   - ein Spaltenname bzw. Spaltenindex, oder
#   - ein Tupel (Muster, Steuerspalte).
# Das Tupel beschreibt einen Wunsch, den REDCap per Branching Logic auf mehrere
# Spalten aufteilt: Die Zweitwunsch-Dropdowns heissen zweitwunschvm_ws1 ...
# zweitwunschvm_ws4, und eingeblendet wird jeweils das Feld, das zum Erstwunsch
# passt (so steht der Erstwunsch beim Zweitwunsch nicht mehr zur Auswahl).
# Gelesen wird dann die Spalte Muster.format(Wert der Steuerspalte).
spaltenname_vorname = "vorname"
spaltenname_name = "nachname"
spaltenname_email = "email"

