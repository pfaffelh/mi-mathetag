import streamlit as st
import socket, os

# Konfiguration für den Mathetag 2025

# Workshopreihen

# kosten[0]: falls man den Erstwunsch bekommt
# kosten[1]: falls man den Zweitwunsch bekommt
# kosten[2]: falls man keinen der beiden Wünschen bekommt

datum = "14.11.2025"

workshopreihe = [
    {
        "name" : "Vormittag",
        "wunschspalten" : [5, 6],
        "kosten" : [0, 2, 5],
        "data" : [{
                "name_kurz" : "Workshop 1: Kartenspiel-Algebra - Die Struktur hinter Dobble", # So steht es in der Ausgabe des Anmeldetools
                "name" : "Workshop 1",
                "titel" : "Kartenspiel-Algebra – die Struktur hinter „Dobble“ (Dr. Ernst August von Hammerstein)",
                "groesse" : 30
            },
            {
                "name_kurz" : "Workshop 2: Hilberts Hotel - Unendlichkeiten in der Mathematik", # So steht es in der Ausgabe des Anmeldetools
                "name" : "Workshop 2",
                "titel" : "Hilberts Hotel - Unendlichkeiten in der Mathematik (Dr. Stefan Ludwig)",
                "groesse" : 30
            },
            {
                "name_kurz" : "Workshop 3: Öffentliches Vereinbaren geheimer Schlüssel", # So steht es in der Ausgabe des Anmeldetools
                "name" : "Workshop 3",
                "titel" : "Öffentliches Vereinbaren geheimer Schlüssel (Prof. Dr. Wolfgang Soergel)",
                "groesse" : 30
            }
        ]
    },
    {
        "name" : "Nachmittag",
        "wunschspalten" : [7, 8],
        "kosten" : [0, 2, 5],
        "data" : [{
                "name_kurz" : "Workshop 4: Die Mathematik des Jonglierens",
                "name" : "Workshop 4",
                "titel" : "Die Mathematik des Jonglierens (Dr. Jonathan Brugger)",
                "groesse" : 30
                },
            {
                "name_kurz" : "Workshop 5: Die unglaubliche Beweis-Maschine",
                "name" : "Workshop 5",
                "titel" : "Die unglaubliche Beweis-Maschine (Prof. Dr. Peter Pfaffelhuber)",
                "groesse" : 30
            },
            {
                "name_kurz" : "Workshop 6: Topologie - ein Papierband ohne Innen und Außen",
                "name" : "Workshop 6",
                "titel" : "Topologie – ein Band aus Papier ohne Innen und Außen (Dr. Maximilian Stegemeyer)",
                "groesse" : 30
            }
        ]
    }
]

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

mail_betreff = "Einteilung für den Mathetag am " + datum

mail_body = """
Hallo {Vorname} {Nachname},
<br>
<br>
wir freuen uns, dich am Freitag zum Mathe-Tag an der Universität Freiburg begrüßen zu dürfen. Wir starten um 8:45 Uhr im Hörsaal II (Obergeschoss) in der <a href="https://www.openstreetmap.org/?mlat=48.002320&mlon=7.847924#map=19/48.002320/7.847924">Albertstraße 23b</a>. Eine Wegbeschreibung findest du auf unserer <a href="https://uni-freiburg.de/mathematik-didaktik/mathematik-tag/">Webseite</a>. 
<br>
Die Workshops haben wir so zugeteilt, dass möglichst viele ihren Erstwunsch bekommen. Dir wurden folgende Workshops zugeteilt:
<br>
<ul>
<li>Vormittag: {EinteilungVormittag}: {WorkshopnameVormittag}</li>
<li>Nachmittag: {EinteilungNachmittag}: {WorkshopnameNachmittag}</li>
</ul>
Am Ende der Veranstaltung erhältst du von uns eine Teilnahmebescheinigung, die du in der Schule vorzeigen kannst.
<br>
<br>
Viele Grüße,
<br>
Dein Mathetag-Team
<br>
<br>
<br>
<p>
    Du erhältst diese Mail, weil Du Dich für den <a href='https://uni-freiburg.de/mathematik-didaktik/mathematik-tag/'>Mathetag des Mathematischen Instituts</a> angemeldet hast. Bei Fragen schreibe bitte direkt an 
    <a href="mailto:didaktik@math.uni-freiburg.de">uns</a>.
</p>
<p>Universität Freiburg<br>
Abteilung Didaktik der Mathematik<br>
Ernst-Zermelo-Str. 1<br>
79104 Freiburg
</p>
<img
    src="https://www.math.uni-freiburg.de/static/images/ufr.png"
    alt="Universität Freiburg"
    width="300"
/>
<br />
"""

workshop_dict = { w["name_kurz"] : w["titel"] for wr in workshopreihe for w in wr["data"] }
workshopname_dict = { w["name_kurz"] : w["name"] for wr in workshopreihe for w in wr["data"] }
workshopsize_dict = { w["name_kurz"] : w["groesse"] for wr in workshopreihe for w in wr["data"] }

for wr in workshopreihe:
    wr["anzahl_wuensche"] = len(wr["wunschspalten"])
    if len(wr["wunschspalten"]) + 1 != len(wr["kosten"]):
        st.error(f"Konfiguration fehlerhaft. In {wr['name']} ist eine falsche Anzahl von Kosten angegeben. (Muss eins mehr als die Anzahl der Wunschspalten sein.)") 

spaltenname_vorname = "Name (Vorspann)"
spaltenname_name = "Name "
spaltenname_email = "E-Mail (E-Mail eingeben)"

