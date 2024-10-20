import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations
from scipy.optimize import linear_sum_assignment
from config import *

st.set_page_config(page_title="Mathetag Einteilung", layout="wide")

# Es liegt eine csv-Datei vor mit Feldern
#id,Nachname,Vorname,Klassenstufe,Schule,Name der Mathematiklehrkraft,Vormittagskurs Erstwunsch, Vormittagskurs Zweitwunsch, Nachmittagskurs Erstwunsch, Nachmittagskurs Zweitwunsch
# Ziel ist es, zwei Spalten zu Ergänzungen: Zuteilung Vormittag, Zuteilung Nachmittag

# In config.py sind die Workshops definiert. Der "name" gibt dabei jeweils den Workshop an

st.header("Einteilung für den Mathetag am 15.11.2024")

st.write("Es werden folgende Workshops angeboten:")
for wr in workshopreihe:
    col0, col1 = st.columns([1,4])
    col0.write(f"{wr['name']}:")
    for w in wr["data"]:
        col1.write(f"{w['name']}: {w['titel']} (Größe {w['groesse']})")
    col1.write(f"**Insgesamt gibt es {wr['groesse']} Plätze.**")
st.write("### Anmeldungen")
st.write("Es liegen Anmeldungen in einer csv-Datei in Folgendem Format vor:")
df = pd.read_csv("anmeldungen.csv", index_col=False)
st.write(df)

anmeldungen_csv = st.file_uploader("Upload Anmeldungen")

if anmeldungen_csv:
    df = pd.read_csv(anmeldungen_csv)
    #df = pd.read_csv("anmeldungen.csv", index_col=False)
    col1.write(f"**Insgesamt gibt es {df.shape[0]} Anmeldungen.**")
    st.write("Nun wird die Einteilung vorgenommen.")
    for wr in workshopreihe:    
        with st.expander(f"Einteilung von {wr["name"]}"):
            if df.shape[1] > wr['groesse']:
                st.write(f"**Einteilung in {wr['name']} nicht möglich, da es {df.shape[1]} Anmeldungen, aber nur {wr['groesse']} Plätze gibt.**")
            else: 
                st.write(f"Einteilung in {wr['name']} möglich, es gibt genug Plätze.")

            # Diese Liste von Listen gibt die Wünsche der Teilnehmer 
            wuensche = [list(df[df.columns[i]]) for i in wr["wunschspalten"]]
            allewuensche = [item for sublist in wuensche for item in sublist]        
            # Wünsche müssen mit den Namen der Workshops übereinstimmen!
            w_namen = [w["name"] for w in wr["data"]]
            #st.write(allewuensche)
            #st.write(w_namen)
            fehler = [w for w in allewuensche if w not in w_namen]
            if len(fehler):
                st.warning(f"Wünsche {fehler} wurden angegeben, sind aber nicht wählbar!")

            # Doppelte Wünsche werden gelöscht:
            for wunsch1, wunsch2 in combinations(wuensche,2):
                for i in range(len(wunsch1)):
                    if wunsch1[i] == wunsch2[i]:
                        wunsch2[i] = ""

            # spalten sind die workshops der einzelnen Reihen, jede Spalte ist ein Platz im Workshop
            spalten = []
            for w in wr["data"]:
                spalten.extend([w['name'] for i in range(w['groesse'])])
            # Zunächst gehen wir von maximalen Kosten aus
            kosten = wr["kosten"][-1] + np.zeros((df.shape[0], len(spalten)))
            for i in range(kosten.shape[0]):
                for j in range(kosten.shape[1]):
                    for w in range(len(wuensche)):
                        if wuensche[w][i] == spalten[j]:
                            kosten[i,j] = float(wr["kosten"][w])
            row_ind, col_ind = linear_sum_assignment(kosten, maximize=False)

            df[f"Einteilung {wr["name"]}"] = [spalten[j] for j in col_ind]
            df[f"Workshopname {wr["name"]}"] = [ workshop_dict[spalten[j]] for j in col_ind ]

            # Ein wenig Statistik
            for wunsch in wuensche:
                st.write(f"{wr["name"]}: {sum(df[f"Einteilung {wr["name"]}"] == wunsch)} Teilnehmer haben ihren Wunsch { wuensche.index(wunsch) + 1} bekommen.")
    st.write("Hier das Ergebnis der Einteilung:")
    st.write(df)
    