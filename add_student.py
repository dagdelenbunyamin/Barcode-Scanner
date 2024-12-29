import sqlite3

# Verbindung zur Datenbank herstellen
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

# Schülerdaten eingeben
barcode_id = input("Gib die Barcode-Nummer (ID) ein: ")
student_name = input("Gib den Namen des Schülers ein: ")

# Daten in die Tabelle einfügen
try:
    cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (barcode_id, student_name))
    connection.commit()
    print(f"Schüler {student_name} mit Barcode-ID {barcode_id} wurde erfolgreich hinzugefügt.")
except sqlite3.IntegrityError:
    print("Fehler: Diese Barcode-ID existiert bereits in der Datenbank.")
finally:
    connection.close()
