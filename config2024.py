import streamlit as st

# Konfiguration für den Mathetag 2024

# Workshopreihen

# kosten[0]: falls man den Erstwunsch bekommt
# kosten[1]: falls man den Zweitwunsch bekommt
# kosten[2]: falls man keinen der beiden Wünschen bekommt

workshopreihe = [
    {
        "name" : "Vormittag",
        "wunschspalten" : [4, 5],
        "kosten" : [0, 2, 5],
        "data" : [{
                "name_kurz" : "ws1",
                "name" : "Workshop 1",
                "titel" : "Modulo-Rechnung und Codierungs-Theorie (Dr. Ernst August von Hammerstein)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws2",
                "name" : "Workshop 2",
                "titel" : "Kreisspiegelungen (Prof. Dr. Wolfgang Soergel)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws3",
                "name" : "Workshop 3",
                "titel" : "Verkehrssimulation (Prof. Dr. Dietmar Kröner)",
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
                "titel" : "Siteswap – eine mathematische Beschreibung von Jongliermustern (Stud. Maja König)",
                "groesse" : 30
                },
            {
                "name_kurz" : "ws5",
                "name" : "Workshop 5",
                "titel" : "Vom Landkartenfärben und Reiseplänen (M. Sc. Mitja Roeder)",
                "groesse" : 30
            },
            {
                "name_kurz" : "ws6",
                "name" : "Workshop 6",
                "titel" : "Wie groß ist unendlich groß? (M.Sc. Charlotte Bartnick)",
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
