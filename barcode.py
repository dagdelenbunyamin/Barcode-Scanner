import streamlit as st
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

# Schülername anhand der Barcode-ID abrufen
def get_student_name(barcode_id):
    with sqlite3.connect('students.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM students WHERE id = ?", (barcode_id,))
        result = cursor.fetchone()
        return result[0] if result else None

# Haupt-App
def main():
    initialize_database()
    st.title("Schülerregistrierung mit Barcode-Scanner-Gerät 📠")

    menu = ["Schüler scannen", "Schüler hinzufügen"]
    choice = st.sidebar.selectbox("Menü auswählen", menu)

    if choice == "Schüler scannen":
        st.subheader("Barcode scannen")
        barcode_id = st.text_input("Scanne den Barcode hier:")
        
        if barcode_id:
            student_name = get_student_name(barcode_id)
            if student_name:
                st.success(f"Schüler erkannt: {student_name}")
            else:
                st.error("Kein Schüler mit dieser Barcode-ID gefunden.")

    elif choice == "Schüler hinzufügen":
        st.subheader("Neuen Schüler hinzufügen")
        barcode_id = st.text_input("Barcode-ID der Schülerkarte:")
        student_name = st.text_input("Name des Schülers:")
        
        if st.button("Hinzufügen"):
            if barcode_id and student_name:
                try:
                    with sqlite3.connect('students.db') as connection:
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (barcode_id, student_name))
                        connection.commit()
                        st.success(f"Schüler {student_name} erfolgreich hinzugefügt.")
                except sqlite3.IntegrityError:
                    st.error("Fehler: Diese Barcode-ID existiert bereits.")
            else:
                st.error("Bitte fülle alle Felder aus.")

if __name__ == "__main__":
    main()
