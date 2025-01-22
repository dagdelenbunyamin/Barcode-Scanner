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

# Barcode scannen mit QuaggaJS
def barcode_scan():
    st.subheader("Barcode scannen")
    st.info("Richte deine Kamera auf den Barcode. Das Ergebnis wird automatisch angezeigt.")

    # QuaggaJS-HTML-Komponente (wird auf der Streamlit-Seite gerendert)
    barcode_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
        <script>
            function startScanner() {
                Quagga.init({
                    inputStream: {
                        name: "Live",
                        type: "LiveStream",
                        target: document.querySelector('#scanner')
                    },
                    decoder: {
                        readers: ["code_128_reader", "ean_reader", "ean_8_reader"]
                    }
                }, function(err) {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    Quagga.start();
                });

                Quagga.onDetected(function(data) {
                    const barcode = data.codeResult.code;
                    // Barcode an Streamlit übergeben
                    window.parent.postMessage({barcode: barcode}, "*");
                    Quagga.stop();
                });
            }
        </script>
    </head>
    <body onload="startScanner()">
        <div id="scanner" style="width: 100%; height: 300px; border: 1px solid black;"></div>
    </body>
    </html>
    """
    # Die HTML-Komponente anzeigen
    st.components.v1.html(barcode_html, height=400)

# Empfang des Barcodes aus der QuaggaJS-Komponente und Speicherung im session_state
def handle_barcode():
    # Warten auf den Barcode von der QuaggaJS-Komponente
    barcode = st.session_state.get('barcode', None)
    if barcode:
        student_name = get_student_name(barcode)
        if student_name:
            st.success("Barcode erfolgreich gescannt!")
            st.write(f"**Schülername:** {student_name}")
            st.write(f"**Barcode-ID:** {barcode}")
            st.write("Der Schüler wurde erfolgreich identifiziert.")
        else:
            st.error("Kein Schüler mit diesem Barcode gefunden. Bitte überprüfe den Barcode oder füge den Schüler hinzu.")

# Haupt-App
def main():
    initialize_database()
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
        barcode_scan()
        handle_barcode()

if __name__ == "__main__":
    main()
