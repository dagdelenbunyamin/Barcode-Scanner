import cv2

# Versuche, die Kamera zu öffnen
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden. Überprüfe den Kamerazugriff.")
else:
    print("Kamera erfolgreich gestartet!")
    cap.release()
