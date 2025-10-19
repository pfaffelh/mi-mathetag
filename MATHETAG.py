import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np
import random
from itertools import combinations
from scipy.optimize import linear_sum_assignment
from edition_2025.config import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header, make_header

st.set_page_config(page_title="Mathetag Einteilung", layout="wide")


def print_readable_email(msg: MIMEMultipart):
    """Gibt eine MIMEMultipart-Nachricht mit dekodierten Headern aus."""
    
    # 1. Header dekodieren und korrigiert ausgeben
    st.write("--- DEKODIERTE HEADER ---")
    for key, value in msg.items():
        # make_header konvertiert die komplexe Kodierung (?=utf-8?...) in einen einfachen String
        decoded_value = str(make_header(decode_header(value)))
        st.write(f"{key}: {decoded_value}")
    
    # 2. Body-Inhalt ausgeben
    st.write("--- E-MAIL BODY (HTML/TEXT) ---")
    if msg.is_multipart():
        # Durch die Teile der Multipart-Nachricht iterieren
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = part.get('Content-Disposition')

            # Nur Text- oder HTML-Teile ohne Anhang berücksichtigen
            if ctype in ('text/plain', 'text/html') and cdisp is None:
                try:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    text = payload.decode(charset) if isinstance(payload, (bytes, bytearray)) else str(payload)

                    st.write(f"Content-Type: {ctype}")
                    if ctype == 'text/html':
                        # Quelltext anzeigen
                        st.code(text, language='html')
                        # Optional: HTML gerendert anzeigen (unsafe_allow_html=True)
                        st.markdown("**Gerendertes HTML:**", unsafe_allow_html=False)
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        # Plain-Text anzeigen
                        st.text(text)
                except Exception as e:
                        st.write(f"[Konnten Teil {ctype} nicht dekodieren: {e}]")
    else:
        # Für einfache (nicht-multipart) Nachrichten
        st.write(msg.get_payload())
    st.write("-------------------------------\n")
    
def to_excel(df, output):
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']

        # Automatische Anpassung der Spaltenbreite an die Inhalte
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter  # Spaltenbuchstabe (z.B., 'A', 'B', 'C')
            for cell in col:
                try:
                    max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = max_length + 2  # +2 für Puffer
            worksheet.column_dimensions[col_letter].width = adjusted_width
    return output.getvalue()


# Es liegt eine xls-Datei vor mit Feldern
# 1. Name (Vorname)	
# 2. Name (zweiter Vorname)	
# 3. Name (Nachname)	
# 4. Name (Nachspann)	
# 5. E-Mail (E-Mail eingeben)	
# 6. Klassenstufe	
# 7. Schule	
# 8. Welche Workshops willst du am Vormittag besuchen?	
# 9. Erstwunsch Vormittag:	
# 10. Zweitwunsch Vormittag (falls der Workshop von Erstwunsch bereits voll ist):	
# 11. Erstwunsch Nachmittag:	
# 12. Zweitwunsch  Nachmittag (falls der Workshop von Erstwunsch bereits voll ist):
# Ziel ist es, zwei Spalten zu Ergänzungen: Zuteilung Vormittag, Zuteilung Nachmittag
# Im Anschluss an die Einteilung werden Mails verschickt.

# In config.py sind die Workshops definiert. Der "name" gibt dabei jeweils den Workshop an

st.header(f"Einteilung für den Mathetag am {datum}")

if "workshopreihe" not in st.session_state:
    st.session_state.workshopreihe = workshopreihe
if "xls_einteilung" not in st.session_state:
    st.session_state.xls_einteilung = ""

def update_groesse(wr, w):
    st.session_state.workshopreihe[st.session_state.workshopreihe.index(wr)]['data'][wr['data'].index(w)]["groesse"] = st.session_state[f"{w['name_kurz']}_size"]

st.write("Es werden folgende Workshops angeboten:")
col = st.columns([1,1,1])

for wr in st.session_state.workshopreihe:
    with col[st.session_state.workshopreihe.index(wr)]:
        st.write(f"{wr['name']}:")
        for w in wr["data"]:
            col0, col1 = st.columns([4,1])
            col0.write(f"{w['name']}: {w['titel']}")
            w['groesse'] = col1.number_input("Größe", min_value = 0, value = w['groesse'], on_change = update_groesse, args = (wr, w,), key = f"{w['name_kurz']}_size")
            st.write("")
        wr["groesse"] = sum([int(w['groesse']) for w in wr['data']])
        st.write(f"**Insgesamt gibt es {wr['groesse']} Plätze.**")
st.write("### Anmeldungen")
st.write("Es liegen Anmeldungen in einer xls-Datei vor:")

anmeldungen_xls = st.file_uploader("Upload Anmeldungen")

if anmeldungen_xls:
    df = pd.read_excel(anmeldungen_xls)
    df = df.drop_duplicates(subset=spaltenname_email, keep='last')
    st.write(f"**Insgesamt gibt es {df.shape[0]} Anmeldungen.**")
    st.write("Nun wird die Einteilung vorgenommen.")
    for wr in st.session_state.workshopreihe:    
        with st.expander(f"Einteilung von {wr["name"]}"):
            if df.shape[1] > wr['groesse']:
                st.write(f"**Einteilung in {wr['name']} nicht möglich, da es {df.shape[1]} Anmeldungen, aber nur {wr['groesse']} Plätze gibt.**")
            else: 
                st.write(f"Einteilung in {wr['name']} möglich, es gibt genug Plätze.")

            # Diese Liste von Listen gibt die Wünsche der Teilnehmer 
            wuensche = [list(df[df.columns[i]]) for i in wr["wunschspalten"]]
            allewuensche = [item for sublist in wuensche for item in sublist]        
            # Wünsche müssen mit den Namen der Workshops übereinstimmen!
            w_namen = [w["name_kurz"] for w in wr["data"]]
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
                spalten.extend([w['name_kurz'] for i in range(w['groesse'])])
            random.seed(42)
            random.shuffle(spalten)
            # Zunächst gehen wir von maximalen Kosten aus
            kosten = wr["kosten"][-1] + np.zeros((df.shape[0], len(spalten)))
            for i in range(kosten.shape[0]):
                for j in range(kosten.shape[1]):
                    for w in range(len(wuensche)):
                        if wuensche[w][i] == spalten[j]:
                            kosten[i,j] = float(wr["kosten"][w])
            row_ind, col_ind = linear_sum_assignment(kosten, maximize=False)

            df[f"Einteilung {wr["name"]}"] = [workshopname_dict[spalten[j]] for j in col_ind]
            df[f"Workshopname {wr["name"]}"] = [ workshop_dict[spalten[j]] for j in col_ind ]

            # Ein wenig Statistik
            for wunsch in wuensche:
                st.write(f"{wr["name"]}: {sum(df[f"Einteilung {wr["name"]}"] == [workshopname_dict[x] for x in wunsch])} Teilnehmer haben ihren Wunsch { wuensche.index(wunsch) + 1} bekommen.")
            for w in wr["data"]:
                st.write(f"Zu {w['name']} sind {sum(df[f"Einteilung {wr["name"]}"] == w["name"])} Teilnehmer eingeteilt.")
    st.write("Hier das Ergebnis der Einteilung:")
    st.write(df)

    output = BytesIO()
    def to_excel(df):
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']

            # Automatische Anpassung der Spaltenbreite an die Inhalte
            for col in worksheet.columns:
                max_length = 0
                col_letter = col[0].column_letter  # Spaltenbuchstabe (z.B., 'A', 'B', 'C')
                for cell in col:
                    try:
                        max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                adjusted_width = max_length + 2  # +2 für Puffer
                worksheet.column_dimensions[col_letter].width = adjusted_width
        return output.getvalue()

    # Streamlit-Button für den Download
    excel_data = to_excel(df)
    st.download_button(
        label="Download Excel-Datei",
        data=excel_data,
        file_name="anmeldungen.xls",
        mime="application/vnd.ms-excel"
    )

with st.expander("Mail-Template", expanded=False):
    st.write(f"Hier ist das Mail-Template. Falls Einträge in den Spalten verwendet werden sollen, schreiben Sie {'{Spaltenname}'}, z.B. {{{spaltenname_vorname}}} für den Vornamen.")
    st.write(f"Die Mails an die Teilnehmer werden von der Mail-Adresse {smtp_user} versendet. Im Postausgang dieser Mail-Adresse befinden sich Kopien der verschickten Mails.")

    st.session_state.mail_betreff = st.text_input("Mail-Betreff", value=mail_betreff, key="mail_betreff1")
    st.session_state.mail_body = st.text_area("Mail-Template", value=mail_body, height=300, key="mail_template1")

st.session_state.xls_einteilung = st.file_uploader("Einteilung für den Versand (xls)", key = "data_einteilung")
st.write("Die Datei hat dieselbe Form wir die soeben heruntergeladene.")
if st.session_state.xls_einteilung:
    df = pd.read_excel(st.session_state.xls_einteilung).fillna("")
    df.fillna("", inplace=True)

    with st.expander("Mails generieren und verschicken"):
        EMAIL_SPALTE = 'Mail'
        NAME_SPALTE = 'Nachname'
        VORNAME_SPALTE = 'Vorname' # Optionale Personalisierung

        for index, row in df.iterrows():
            empfaenger_email = row[spaltenname_email]
            nachname = row[spaltenname_name]
            vorname = row[spaltenname_vorname]
            einteilungVormittag = row["Einteilung Vormittag"]
            workshopnameVormittag = row["Workshopname Vormittag"]
            einteilungNachmittag = row["Einteilung Nachmittag"]
            workshopnameNachmittag = row["Workshopname Nachmittag"]

            # Personalisierung des Betreffs und des Body
            personalisierte_betreff = st.session_state.mail_betreff.format(Nachname=nachname, Vorname=vorname)
            personalisierte_body = st.session_state.mail_body.format(Nachname=nachname, Vorname=vorname, EinteilungVormittag = einteilungVormittag, WorkshopnameVormittag = workshopnameVormittag, EinteilungNachmittag = einteilungNachmittag, WorkshopnameNachmittag = workshopnameNachmittag)

            # E-Mail-Objekt erstellen (MIMEMultipart für HTML-Inhalte)
            msg = MIMEMultipart()
            msg['From'] = smtp_user 
            # msg['Reply-To'] = "noreply@math.uni-freiburg.de" 
            msg['To'] = empfaenger_email
            msg['Subject'] = personalisierte_betreff
            msg.attach(MIMEText(personalisierte_body, 'html')) # Inhalt als HTML hinzufügen                
            print_readable_email(msg)

        send_mails = st.button("Emails verschicken")
        if send_mails: 
            for index, row in df.iterrows():
                empfaenger_email = row[spaltenname_email]
                nachname = row[spaltenname_name]
                vorname = row[spaltenname_vorname]
                einteilungVormittag = row["Einteilung Vormittag"]
                workshopnameVormittag = row["Workshopname Vormittag"]
                einteilungNachmittag = row["Einteilung Nachmittag"]
                workshopnameNachmittag = row["Workshopname Nachmittag"]

                # Personalisierung des Betreffs und des Body
                personalisierte_betreff = mail_betreff.format(Nachname=nachname, Vorname=vorname)
                personalisierte_body = mail_body.format(Nachname=nachname, Vorname=vorname, EinteilungVormittag = einteilungVormittag, WorkshopnameVormittag = workshopnameVormittag, EinteilungNachmittag = einteilungNachmittag, WorkshopnameNachmittag = workshopnameNachmittag)

                # E-Mail-Objekt erstellen (MIMEMultipart für HTML-Inhalte)
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = empfaenger_email
                msg['Subject'] = personalisierte_betreff
                msg.attach(MIMEText(personalisierte_body, 'html')) # Inhalt als HTML hinzufügen                
                with smtplib.SMTP_SSL("mail.uni-freiburg.de", 465) as server:
                    server.login(smtp_user, smtp_password)
                    print("Erfolgreich eingeloggt!")
                    server.send_message(msg)
                    print(f"E-Mail an {empfaenger_email} erfolgreich versendet!")
                    server.quit()
