import streamlit as st
import sqlite3
import cv2
import numpy as np

# Datenbank erstellen/verwalten
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

# Schüler zur Datenbank hinzufügen
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

# Schülername anhand der Barcode-ID abrufen
def get_student_name(barcode_id):
    with sqlite3.connect('students.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM students WHERE id = ?", (barcode_id,))
        result = cursor.fetchone()
        return result[0] if result else None

# Barcode mit OpenCV scannen
def scan_barcode(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(gray)
    return decoded_info

# Live-Scanner starten
def start_scanner():
    cap = cv2.VideoCapture(0)  # Kamera starten
    if not cap.isOpened():
        st.error("Kamera konnte nicht geöffnet werden. Bitte überprüfe die Kameraeinstellungen.")
        return

    st.write("**Drücke 'Scanner stoppen', um den Scanner zu beenden.**")
    stop_button = st.button("Scanner stoppen")

    scanned_student = None
    frame_placeholder = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Fehler beim Lesen des Kamerabildes.")
            break

        barcodes = scan_barcode(frame)
        for barcode in barcodes:
            barcode_data = barcode
            student_name = get_student_name(barcode_data)

            # Rahmen um den Barcode zeichnen (optional)
            pts = np.array(barcode.polygon, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # Ergebnistext anzeigen
            text = f"{student_name} ({barcode_data})" if student_name else f"Unbekannt ({barcode_data})"
            cv2.putText(frame, text, (barcode.rect.left, barcode.rect.top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # Schüler gefunden -> anzeigen und stoppen
            if student_name:
                scanned_student = student_name
                st.success(f"Schüler erkannt: **{student_name}**")
                stop_button = True
                break

        # Live-Kamerastream anzeigen
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        if stop_button:
            break

    cap.release()
    cv2.destroyAllWindows()
    st.info("Scanner gestoppt.")

    if not scanned_student:
        st.warning("Kein gültiger Barcode erkannt.")

# Haupt-App
def main():
    initialize_database()  # Datenbank initialisieren
    st.title("Schülerregistrierung mit Barcode-Scanner 📷")

    menu = ["Schüler hinzufügen", "Barcode scannen"]
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

if __name__ == "__main__":
    main()
