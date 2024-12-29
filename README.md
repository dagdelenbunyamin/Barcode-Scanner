# Barcode-Scanner für Schülerregistrierung

Dieses Projekt ist ein **Barcode-Scanner**-Tool, das mit **Streamlit**, **OpenCV**, **SQLite** und weiteren Python-Modulen erstellt wurde. Es dient dazu, Schülerdaten mit Barcode-IDs zu verwalten. Die Anwendung kann Barcodes scannen, den zugehörigen Schülernamen aus einer Datenbank abrufen und neue Schüler zur Datenbank hinzufügen.

## Funktionen:
- **Schüler hinzufügen**: Barcode-ID und Name des Schülers werden in einer SQLite-Datenbank gespeichert.
- **Barcode scannen**: Der Barcode wird live gescannt und der zugehörige Schülername angezeigt.
- **Echtzeit-Scanner**: Die Anwendung zeigt den Kamerastream an und erkennt Barcodes automatisch.

## Abhängigkeiten:
Die folgenden Python-Module werden benötigt:
- `streamlit`
- `opencv-python`
- `pyzbar`
- `numpy`
- `sqlite3`

### Installation der Abhängigkeiten:
Erstelle eine virtuelle Umgebung (optional):
```bash
python -m venv venv

##### Aktiviere die virtuelle Umgebung:

- `Windows:`
.\venv\Scripts\activate

- `Mac/Linux:`:
source venv/bin/activate

# Benutzung

### Starte die Streamlit-App:
```bash
streamlit run main.py

