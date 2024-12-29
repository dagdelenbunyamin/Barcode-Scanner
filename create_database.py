import sqlite3

# Verbindung zur Datenbank herstellen (die Datenbank wird erstellt, falls sie nicht existiert)
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

# Tabelle erstellen, falls sie nicht existiert
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT UNIQUE,
    name TEXT NOT NULL
)
''')

# Beispiel-Daten hinzufügen
try:
    cursor.execute("INSERT INTO students (student_number, name) VALUES (?, ?)", ("123456789", "Ali Yilmaz"))
    cursor.execute("INSERT INTO students (student_number, name) VALUES (?, ?)", ("987654321", "Fatma Demir"))
    connection.commit()
    print("Beispiel-Daten hinzugefügt.")
except sqlite3.IntegrityError:
    print("Beispiel-Daten bereits vorhanden.")

# Verbindung schließen
connection.close()
