import streamlit as st
import sqlite3
import cv2
from pyzbar.pyzbar import decode
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

        # JavaScript einfügen
        st.components.v1.html("""
        <script>
        async function startCamera() {
            const video = document.createElement("video");
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.play();

            document.body.appendChild(video);
        }
        startCamera();
        </script>
        """, height=300)

if __name__ == "__main__":
    main()
