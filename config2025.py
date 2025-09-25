import streamlit as st

# Konfiguration für den Mathetag 2024

# Workshopreihen

# kosten[0]: falls man den Erstwunsch bekommt
# kosten[1]: falls man den Zweitwunsch bekommt
# kosten[2]: falls man keinen der beiden Wünschen bekommt

datum = "14.11.2025"

workshopreihe = [
    {
        "name" : "Vormittag",
        "wunschspalten" : [4, 5],
        "kosten" : [0, 2, 5],
        "data" : [{
                "name_kurz" : "ws1",
                "name" : "Workshop 1",
                "titel" : "Kartenspiel-Algebra – die Struktur hinter „Dobble“ (Dr. Ernst August von Hammerstein)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws2",
                "name" : "Workshop 2",
                "titel" : "TBA (Dr. Stefan Ludwig)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws3",
                "name" : "Workshop 3",
                "titel" : "Öffentliches Vereinbaren geheimer Schlüssel (Prof. Dr. Wolfgang Soergel)",
                "groesse" : 30
            }
        ]
    },
    {
        "name" : "Nachmittag",
        "wunschspalten" : [6, 7],
        "kosten" : [0, 2, 5],
        "data" : [{
                "name_kurz" : "ws4",
                "name" : "Workshop 4",
                "titel" : "Die Mathematik des Jonglierens (Dr. Jonathan Brugger)",
                "groesse" : 30
                },
            {
                "name_kurz" : "ws5",
                "name" : "Workshop 5",
                "titel" : "Die unglaubliche Beweis-Maschine (Prof. Dr. Peter Pfaffelhuber)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws6",
                "name" : "Workshop 6",
                "titel" : "Topologie – ein Band aus Papier ohne Innen und Außen (Dr. Maximilian Stegemeyer)",
                "groesse" : 30
            }
        ]
    }
]

workshop_dict = { w["name_kurz"] : w["titel"] for wr in workshopreihe for w in wr["data"] }
workshopname_dict = { w["name_kurz"] : w["name"] for wr in workshopreihe for w in wr["data"] }
workshopsize_dict = { w["name_kurz"] : w["groesse"] for wr in workshopreihe for w in wr["data"] }

for wr in workshopreihe:
    wr["anzahl_wuensche"] = len(wr["wunschspalten"])
    if len(wr["wunschspalten"]) + 1 != len(wr["kosten"]):
        st.error(f"Konfiguration fehlerhaft. In {wr['name']} ist eine falsche Anzahl von Kosten angegeben. (Muss eins mehr als die Anzahl der Wunschspalten sein.)") 
