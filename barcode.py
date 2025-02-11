import streamlit as st
import sqlite3
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# --- Benutzerverwaltung für Login ---
USER_CREDENTIALS = {"admin": "flb23"}

# --- Datenbank erstellen/verwalten ---
def initialize_database():
    with sqlite3.connect('students.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        connection.commit()

# --- Schüler zur Datenbank hinzufügen ---
def add_student(barcode_id, student_name):
    try:
        with sqlite3.connect('students.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (barcode_id, student_name))
            connection.commit()
            return f"Schüler {student_name} mit Barcode-ID {barcode_id} erfolgreich hinzugefügt."
    except sqlite3.IntegrityError:
        return "Fehler: Diese Barcode-ID existiert bereits in der Datenbank."
    except sqlite3.Error as e:
        return f"Datenbankfehler: {e}"

# --- Schülername anhand der Barcode-ID abrufen ---
def get_student_name(barcode_id):
    with sqlite3.connect('students.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM students WHERE id = ?", (barcode_id,))
        result = cursor.fetchone()
        return result[0] if result else None

# --- Live-Scanner starten ---
def start_scanner():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Kamera konnte nicht geöffnet werden. Bitte überprüfe die Kameraeinstellungen.")
        return

    st.write("**Drücke 'Scanner stoppen', um den Scanner zu beenden.**")
    stop_button = st.button("Scanner stoppen")
    frame_placeholder = st.empty()

    while not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.error("Fehler beim Lesen des Kamerabildes.")
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            student_name = get_student_name(barcode_data)
            text = f"{student_name} ({barcode_data})" if student_name else f"Unbekannt ({barcode_data})"
            cv2.putText(frame, text, (barcode.rect.left, barcode.rect.top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            if student_name:
                stop_button = True
                st.success(f"Schüler erkannt: **{student_name}**")
                break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
    st.info("Scanner gestoppt.")

# --- Impressum und Datenschutz ---
def impressum():
    st.title("📄 Impressum")
    st.markdown("""
    **Verantwortlich für den Inhalt:**
    
    Bünyamin Dagdelen  
    Im Johdorf 1  
    53227 Bonn  
    Deutschland  
    E-Mail: dagdelenbunyamin023@gmail.com
    """)

def datenschutz():
    st.title("🔒 Datenschutz")
    st.markdown("""
    **Datenschutzerklärung**

    Der Schutz Ihrer personenbezogenen Daten ist uns ein besonderes Anliegen. Nachfolgend möchten wir Sie darüber informieren, welche Daten im Rahmen der Nutzung der **Barcode-Scanner-Anwendung für Schülerregistrierung** verarbeitet werden, zu welchem Zweck diese erhoben werden und welche Rechte Ihnen als betroffene Person gemäß der Datenschutz-Grundverordnung (DSGVO) zustehen.

    Diese Anwendung wurde mit **Streamlit** entwickelt, einem Open-Source-Framework für Python-basierte Webanwendungen, das hohe Sicherheitsstandards erfüllt.

    ## 1. Verantwortliche Stelle

    Die verantwortliche Stelle für die Erhebung, Verarbeitung und Nutzung Ihrer personenbezogenen Daten im Rahmen dieser Anwendung ist:

    **Bünyamin Dagdelen**  
    Im Johdorf 1  
    53227 Bonn  
    Deutschland  
    E-Mail: [dagdelenbunyamin023@gmail.com](mailto:dagdelenbunyamin023@gmail.com)  
    Telefon: +49 152 01476523

    Wenn Sie Fragen zum Thema Datenschutz haben, können Sie sich jederzeit an die oben genannte Kontaktadresse wenden.

    ## 2. Erhobene Daten und Verarbeitungszwecke

    Wir erheben und verarbeiten ausschließlich die personenbezogenen Daten, die für die Nutzung der Barcode-Scanner-Anwendung erforderlich sind:

    - **Barcode-ID**: Identifikation des Schülers zur Zuordnung zur entsprechenden Person
    - **Schülername**: Erforderlich, um die Barcode-ID mit dem Namen des Schülers zu verknüpfen
    - **Zeitstempel (optional)**: Dokumentation des Scanvorgangs für interne Zwecke (z.B. zur Nachverfolgung von Scans)

    Die Daten werden **nicht nur lokal gespeichert**, sondern auch auf einem zentralen Server verarbeitet und gespeichert. Dieser Server ist durch **SSH-Verbindungen** gesichert, um sicherzustellen, dass der Datenverkehr zwischen den Geräten und dem Server verschlüsselt ist.

    ## 3. Speicherung und Löschung der Daten

    - Die erfassten Daten werden auf einem **zentralen Server** gespeichert, der nur autorisierten Administratoren zugänglich ist.
    - Für den sicheren Datentransfer wird eine **SSH-Verbindung** verwendet, die alle Daten verschlüsselt, um die Vertraulichkeit zu gewährleisten.
    - Die Daten bleiben so lange gespeichert, wie dies für die Nutzung der Anwendung erforderlich ist, oder bis sie manuell vom Nutzer oder Administrator gelöscht werden.
    - Eine Löschung der Daten kann jederzeit auf Anfrage durch den betroffenen Schüler oder Administrator erfolgen.

    ## 4. Sicherheit der Daten

    Der Schutz Ihrer personenbezogenen Daten wird durch geeignete technische und organisatorische Maßnahmen gewährleistet:

    - **Zentrale Speicherung**: Alle Daten werden auf einem zentralen Server gespeichert, der vor unbefugtem Zugriff geschützt ist.
    - **SSH-Verschlüsselung**: Die Datenübertragung zwischen den Geräten und dem Server erfolgt über eine sichere SSH-Verbindung.
    - **Zugriffskontrollen**: Nur autorisierte Administratoren haben Zugang zu den gespeicherten Daten.
    - **Datenverschlüsselung**: Für die Übertragung der Daten wird eine Verschlüsselung (z.B. HTTPS, SSH) empfohlen, um die Vertraulichkeit der Kommunikation zu sichern.

    ## 5. Nutzung von Streamlit

    Diese Anwendung basiert auf **Streamlit**, einer Open-Source-Plattform, die es ermöglicht, interaktive Webanwendungen zu erstellen. Streamlit stellt sicher, dass die Anwendung sicher und datenschutzkonform betrieben werden kann. Weitere Informationen zu Streamlit finden Sie unter: [https://streamlit.io](https://streamlit.io)

    ## 6. Ihre Rechte als betroffene Person

    Im Hinblick auf die Verarbeitung Ihrer personenbezogenen Daten haben Sie gemäß der DSGVO folgende Rechte:

    - **Recht auf Auskunft**: Sie können jederzeit Auskunft über die bei uns gespeicherten personenbezogenen Daten anfordern.
    - **Recht auf Berichtigung**: Sollten Ihre Daten unrichtig oder unvollständig sein, können Sie eine Korrektur verlangen.
    - **Recht auf Löschung**: Sie können die Löschung Ihrer Daten verlangen, soweit dies gesetzlich möglich ist.
    - **Recht auf Einschränkung der Verarbeitung**: Unter bestimmten Bedingungen können Sie die Verarbeitung Ihrer personenbezogenen Daten einschränken.

    Zur Wahrnehmung dieser Rechte können Sie sich jederzeit an die oben genannte verantwortliche Stelle wenden.

    ## 7. Änderungen dieser Datenschutzerklärung

    Wir behalten uns vor, diese Datenschutzerklärung bei Bedarf zu aktualisieren. Eine Änderung erfolgt insbesondere bei Anpassungen an rechtliche Vorgaben oder der Erweiterung der Funktionen der Anwendung. Die jeweils aktuelle Version der Datenschutzerklärung wird auf dieser Seite veröffentlicht.

    Letzte Aktualisierung: **[Datum einfügen]**
    """)

# --- Cookies-Hinweis ---
def cookies_notice():
    if "cookies_accepted" not in st.session_state:
        st.session_state["cookies_accepted"] = False

    if not st.session_state["cookies_accepted"]:
        st.warning("🍪 Diese Anwendung verwendet Cookies. Durch die Nutzung stimmen Sie der Verwendung zu.")
        if st.button("Akzeptieren"):
            st.session_state["cookies_accepted"] = True
            st.rerun()  # Korrektur hier!

# --- Login-Seite ---
def login_page():
    st.title("🔐 Login zur Schülerregistrierung")

    username = st.text_input("Benutzername:")
    password = st.text_input("Passwort:", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()  # Korrigierte Version
        else:
            st.error("Falscher Benutzername oder Passwort!")

# --- Haupt-App ---
def main():
    initialize_database()
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_page()
        return
    cookies_notice()
    st.title("📷 Schülerregistrierung mit Barcode-Scanner")
    menu = ["Schüler hinzufügen", "Barcode scannen", "📄 Impressum", "🔒 Datenschutz"]
    choice = st.sidebar.selectbox("Menü auswählen", menu)
    if choice == "Schüler hinzufügen":
        st.subheader("Neuen Schüler hinzufügen")
        barcode_id = st.text_input("Barcode-ID der Schülerkarte:")
        student_name = st.text_input("Name des Schülers:")
        if st.button("Hinzufügen"):
            if barcode_id and student_name:
                result = add_student(barcode_id, student_name)
                st.success(result)
            else:
                st.error("Bitte fülle alle Felder aus.")
    elif choice == "Barcode scannen":
        st.subheader("Barcode-Scanner starten")
        st.info("Der Scanner erkennt automatisch die Schülerkarte und zeigt den Namen an.")
        if st.button("Scanner starten"):
            start_scanner()
    elif choice == "📄 Impressum":
        impressum()
    elif choice == "🔒 Datenschutz":
        datenschutz()

if __name__ == "__main__":
    main()
