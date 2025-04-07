import streamlit as st
import sqlite3
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# --- Benutzerverwaltung für Login ---
USER_CREDENTIALS = {"admin": "flb23"}

# --- Datenbank-Pfad ---
DB_PATH = "/home/flb/Barcode/students.db"

# --- Datenbank erstellen/verwalten ---
def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
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
        with sqlite3.connect(DB_PATH) as connection:
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
    with sqlite3.connect(DB_PATH) as connection:
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
    ...  
    ..... 
    Deutschland  
    E-Mail: .....
    """)

def datenschutz():
    st.title("🔒 Datenschutz")
    st.markdown("""
    **Datenschutzerklärung**

    Der Schutz Ihrer personenbezogenen Daten ist uns ein besonderes Anliegen. Wir möchten, dass Sie sich beim Besuch unserer Webanwendung sicher und wohl fühlen. Daher nehmen wir den Schutz Ihrer Daten sehr ernst und erheben, verarbeiten und speichern Ihre personenbezogenen Daten ausschließlich gemäß der **Datenschutz-Grundverordnung (DSGVO)** sowie weiterer geltender Datenschutzgesetze.

    Im Folgenden möchten wir Sie ausführlich darüber informieren, wie und warum wir personenbezogene Daten im Rahmen der Nutzung der **Barcode-Scanner-Anwendung** für die Schülerregistrierung erheben, verarbeiten und speichern, sowie über Ihre Rechte als betroffene Person. Zudem erläutern wir, wie wir mit **Cookies** umgehen, die beim Einsatz der Anwendung verwendet werden.

    ### 1. Verantwortliche Stelle

    Verantwortlich für die Verarbeitung Ihrer personenbezogenen Daten im Rahmen dieser Anwendung ist:

    **Bünyamin Dagdelen**  
    ....  
    ......
    Deutschland  
    E-Mail: [......](mailto:....)  
    Telefon: .....

    Für Fragen zum Thema Datenschutz können Sie sich jederzeit an die oben genannte Kontaktadresse wenden. Ihre Anfragen werden umgehend bearbeitet.

    ### 2. Art und Umfang der erhobenen Daten

    Wir erheben und verarbeiten ausschließlich die Daten, die für die Nutzung der **Barcode-Scanner-Anwendung** erforderlich sind. Dies umfasst insbesondere:

    - **Barcode-ID**: Ein eindeutiger Identifikator, der dem jeweiligen Schüler zugeordnet wird, um diese Person eindeutig identifizieren zu können.
    - **Schülername**: Zur Verknüpfung der Barcode-ID mit dem vollständigen Namen des Schülers, um die Identifikation zu ermöglichen.
    - **Zeitstempel (optional)**: Ein Zeitstempel des Scans zur internen Dokumentation und Verfolgung der Nutzung (z.B. zur Nachverfolgung von Scan-Vorgängen).

    Darüber hinaus verwenden wir **Cookies**, um den Benutzern die Anmeldung zu ermöglichen und deren Sitzung innerhalb der Anwendung aufrechtzuerhalten. Cookies ermöglichen es uns, Ihre Präferenzen zu speichern und die Benutzererfahrung zu verbessern. Sie werden vor der Nutzung der Anwendung um Ihre Zustimmung gebeten, um sicherzustellen, dass Sie der Verwendung von Cookies zustimmen.

    #### 2.1. Zweck der Datenerhebung

    Die erhobenen personenbezogenen Daten werden ausschließlich zu folgenden Zwecken verarbeitet:

    - **Authentifizierung und Benutzerverwaltung**: Die Barcode-ID und der Name des Schülers dienen der eindeutigen Identifikation des Benutzers, um eine sichere Anmeldung und die korrekte Zuordnung zur Anwendung zu gewährleisten.
    - **Zeitliche Erfassung von Scan-Vorgängen**: Der Zeitstempel wird optional erfasst, um eine nachvollziehbare Dokumentation der Nutzung zu ermöglichen.
    - **Verbesserung der Anwendung**: Die erhobenen Daten sowie Cookies tragen dazu bei, dass die Anwendung reibungslos funktioniert und der Benutzer sich während der Sitzung angemeldet und verifiziert bleibt.

    ### 3. Rechtsgrundlage für die Datenverarbeitung

    Die Verarbeitung Ihrer personenbezogenen Daten erfolgt auf Basis der **Datenschutz-Grundverordnung (DSGVO)**, insbesondere:

    - **Art. 6 Abs. 1 lit. a DSGVO** – Einwilligung: Ihre Zustimmung zur Verarbeitung der personenbezogenen Daten im Zusammenhang mit der Nutzung der Anwendung und der Zustimmung zu Cookies.
    - **Art. 6 Abs. 1 lit. b DSGVO** – Vertragserfüllung: Die Daten werden verarbeitet, um Ihnen die Nutzung der Anwendung zu ermöglichen und Ihre Anmeldung zu verwalten.

    ### 4. Speicherung und Löschung der Daten

    Die erhobenen Daten werden auf einem **zentralen, sicheren Server** gespeichert, der nur autorisierten Administratoren zugänglich ist. Alle Daten werden gemäß den geltenden Sicherheitsstandards und unter Berücksichtigung der **DSGVO** verarbeitet.

    - **Speicherfrist**: Die Daten werden nur so lange gespeichert, wie dies für die Nutzung der Anwendung erforderlich ist, oder bis sie auf Antrag des Benutzers oder eines Administrators gelöscht werden.
    - **Löschung auf Anfrage**: Sie können jederzeit die Löschung Ihrer Daten verlangen, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen. Diese Anfrage können Sie über die oben angegebenen Kontaktinformationen stellen.

    Für die Sicherstellung des Schutzes und der Integrität Ihrer Daten wird die **SSH-Verschlüsselung** verwendet. Alle übertragenen Daten zwischen den Benutzern und dem Server sind dadurch verschlüsselt.

    ### 5. Nutzung von Cookies

    **Cookies** sind kleine Textdateien, die beim Besuch einer Website auf Ihrem Endgerät gespeichert werden. Diese ermöglichen es, dass die Anwendung sich an Ihre Einstellungen und Präferenzen erinnert und eine verbesserte Benutzererfahrung bietet. Wir verwenden **essenzielle Cookies**, die unbedingt erforderlich sind, um die grundlegenden Funktionen der Anwendung wie das Login und die Sitzung zu ermöglichen.

    - **Login-Cookies**: Diese Cookies speichern Ihre Anmeldedaten, sodass Sie nicht bei jedem Besuch erneut eingeloggt werden müssen.
    - **Sitzungs-Cookies**: Diese Cookies ermöglichen es, dass Ihre Sitzung aufrechterhalten wird, während Sie durch die Anwendung navigieren.
  
    Beim ersten Besuch der Anwendung wird ein Cookie-Banner angezeigt, in dem Sie um Ihre Zustimmung zur Verwendung von Cookies gebeten werden. Wenn Sie der Verwendung zustimmen, setzen wir die notwendigen Cookies. Sie können diese Einwilligung jederzeit widerrufen, indem Sie die Cookies in den **Browser-Einstellungen** löschen.

    Weitere Informationen zu den verwendeten Cookies finden Sie im Cookie-Manager der Anwendung.

    ### 6. Sicherheit der Daten

    Der Schutz Ihrer personenbezogenen Daten wird durch **technische und organisatorische Maßnahmen** gewährleistet, die einen sicheren Umgang mit den Daten sicherstellen:

    - **Verschlüsselung**: Alle übertragenen Daten werden durch **SSH-** oder **HTTPS-Verschlüsselung** gesichert.
    - **Zugriffskontrollen**: Nur autorisierte Administratoren haben Zugriff auf die gespeicherten Daten.
    - **Backup und Recovery**: Es werden regelmäßige Backups durchgeführt, um Daten im Falle eines technischen Problems wiederherstellen zu können.

    ### 7. Ihre Rechte als betroffene Person

    Im Hinblick auf die Verarbeitung Ihrer personenbezogenen Daten haben Sie gemäß der **DSGVO** folgende Rechte:

    - **Recht auf Auskunft**: Sie haben das Recht, jederzeit Auskunft über die gespeicherten personenbezogenen Daten zu verlangen.
    - **Recht auf Berichtigung**: Sollten Ihre Daten unrichtig oder unvollständig sein, haben Sie das Recht, eine Berichtigung zu verlangen.
    - **Recht auf Löschung**: Sie können jederzeit die Löschung Ihrer Daten verlangen, soweit keine gesetzlichen Aufbewahrungspflichten bestehen.
    - **Recht auf Einschränkung der Verarbeitung**: Unter bestimmten Umständen können Sie die Verarbeitung Ihrer personenbezogenen Daten einschränken lassen.
    - **Recht auf Datenübertragbarkeit**: Sie haben das Recht, Ihre Daten in einem strukturierten, gängigen und maschinenlesbaren Format zu erhalten.
  
    Für die Wahrnehmung dieser Rechte können Sie sich jederzeit an die oben genannte verantwortliche Stelle wenden.

    ### 8. Verwendung von Drittanbietern und Links zu externen Webseiten

    Unsere Anwendung verwendet **keine externen Drittanbieter** für die Verarbeitung Ihrer personenbezogenen Daten, außer die Plattform **Streamlit**, die die zugrunde liegende Infrastruktur bereitstellt. Wir übernehmen keine Verantwortung für den Inhalt und die Datenschutzpraktiken von externen Webseiten, die möglicherweise über Links auf unserer Anwendung zugänglich sind.

    ### 9. Änderungen dieser Datenschutzerklärung

    Wir behalten uns vor, diese Datenschutzerklärung regelmäßig zu aktualisieren, insbesondere wenn neue rechtliche Anforderungen bestehen oder wenn die Funktionen der Anwendung erweitert werden. Alle Änderungen werden auf dieser Seite veröffentlicht, und wir empfehlen, diese regelmäßig zu überprüfen.

    **Letzte Aktualisierung**: **11.02.2025**
    """)

# --- Cookies-Hinweis ---
def cookies_notice():
    if "cookies_accepted" not in st.session_state:
        st.session_state["cookies_accepted"] = False

    if not st.session_state["cookies_accepted"]:
        st.warning("🍪 Diese Anwendung verwendet Cookies. Durch die Nutzung stimmen Sie der Verwendung zu.")
        if st.button("Akzeptieren"):
            st.session_state["cookies_accepted"] = True
            st.rerun()

# --- Login-Seite ---
def login_page():
    st.title("🔐 Login zur Schülerregistrierung")

    username = st.text_input("Benutzername:")
    password = st.text_input("Passwort:", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()  # Korrektur hier
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
