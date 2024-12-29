import streamlit as st
from PIL import Image
import cv2
import numpy as np
import sqlite3

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

# Barcode aus einem Bild scannen
def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # Barcode-Erkennung mit OpenCV
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(gray)
    return decoded_info

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
        st.subheader("Barcode aus Bild scannen")
        st.info("Lade ein Bild mit dem Barcode hoch.")
        uploaded_file = st.file_uploader("Lade ein Bild mit Barcode hoch", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            barcodes = process_image(uploaded_file)
            if barcodes:
                for barcode in barcodes:
                    student_name = get_student_name(barcode)
                    st.write(f"Erkannter Barcode: {barcode}")
                    if student_name:
                        st.success(f"Schüler erkannt: **{student_name}**")
                    else:
                        st.warning(f"Barcode {barcode} ist nicht in der Datenbank.")
            else:
                st.warning("Kein Barcode im Bild erkannt.")

if __name__ == "__main__":
    main()
