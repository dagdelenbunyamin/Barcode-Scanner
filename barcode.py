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
    **Datenschutzerklärung:**
    
## 1. Einleitung
Wir nehmen den Schutz Ihrer personenbezogenen Daten sehr ernst. Diese Datenschutzerklärung informiert Sie darüber, welche Daten durch die **Barcode-Scanner-Anwendung für Schülerregistrierung** verarbeitet werden, zu welchem Zweck dies geschieht und welche Rechte Sie als betroffene Person haben.

Diese Anwendung wurde mit **Streamlit** entwickelt, einem Open-Source-Framework für Python-basierte Webanwendungen, das Sicherheit und Datenschutz gewährleistet.

## 2. Verantwortliche Stelle
Verantwortlich für die Verarbeitung personenbezogener Daten im Rahmen dieser Anwendung ist:

- **Bünyamin Dagdelen**  
- **Im Johdorf 1**  
- **53227 Bonn**  
- **+49 152 01476523**  

Falls Sie Fragen zum Datenschutz haben, können Sie sich jederzeit an die oben genannte Stelle wenden.

## 3. Erhobene Daten und Verarbeitungszweck
Unsere Anwendung verarbeitet nur die Daten, die für die Schülerregistrierung notwendig sind:

- **Barcode-ID**: Identifikation des Schülers
- **Schülername**: Zuordnung zur Barcode-ID
- **Zeitstempel (optional)**: Dokumentation des Scan-Vorgangs

Die Datenverarbeitung erfolgt ausschließlich **lokal auf dem Gerät**, auf dem die Anwendung ausgeführt wird. Eine Weitergabe an Dritte oder externe Server erfolgt **nicht**.

## 4. Speicherung und Löschung der Daten
- Alle erfassten Daten werden **lokal in einer SQLite-Datenbank gespeichert**.
- Daten bleiben gespeichert, bis sie manuell gelöscht werden oder die Anwendung deinstalliert wird.
- Auf Wunsch können Schülerdaten aus der Datenbank entfernt werden.

## 5. Sicherheit und Schutz der Daten
Wir setzen technische und organisatorische Maßnahmen ein, um Ihre Daten vor Manipulation, Verlust oder unbefugtem Zugriff zu schützen:

- **Lokale Speicherung:** Keine Übertragung an Dritte oder in die Cloud.
- **Verschlüsselung:** Die Kommunikation zwischen Benutzer und Anwendung kann über HTTPS gesichert werden.
- **Zugriffsbeschränkung:** Nur autorisierte Personen können auf die Daten zugreifen.

## 6. Nutzung von Streamlit und Sicherheit
Die Anwendung basiert auf **Streamlit**, einer Open-Source-Technologie für sichere Webanwendungen in Python. Streamlit ist darauf ausgelegt, eine einfache und sichere App-Entwicklung zu ermöglichen.

Weitere Informationen zu Streamlit: [https://streamlit.io](https://streamlit.io)

## 7. Ihre Rechte als betroffene Person
Nach der DSGVO haben Sie folgende Rechte in Bezug auf Ihre gespeicherten Daten:

- **Recht auf Auskunft**: Sie können eine Kopie Ihrer gespeicherten Daten anfordern.
- **Recht auf Berichtigung**: Falls Ihre Daten fehlerhaft sind, können Sie eine Korrektur verlangen.
- **Recht auf Löschung**: Sie können verlangen, dass Ihre Daten dauerhaft gelöscht werden.
- **Recht auf Einschränkung der Verarbeitung**: Unter bestimmten Bedingungen können Sie die Verarbeitung Ihrer Daten einschränken.

Zur Geltendmachung Ihrer Rechte kontaktieren Sie uns bitte unter den oben angegebenen Kontaktdaten.

## 8. Änderungen dieser Datenschutzerklärung
Wir behalten uns vor, diese Datenschutzerklärung bei Bedarf zu aktualisieren, um rechtliche Anforderungen oder neue Funktionalitäten der Anwendung zu berücksichtigen.

Letzte Aktualisierung: [Datum einfügen]
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
