import streamlit as st
from PIL import Image
import cv2
import numpy as np

# Barcode-Erkennung mit OpenCV QRCodeDetector
def process_image(uploaded_file):
    # Bild laden
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Barcode-Erkennung
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()

    # QR-Code scannen
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(gray)
    
    return decoded_info

# Streamlit GUI
def main():
    st.title("Barcode-Scanner ohne pyzbar")

    # Bild-Upload
    uploaded_file = st.file_uploader("Lade ein Bild mit Barcode hoch", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Barcode scannen
        barcodes = process_image(uploaded_file)
        
        if barcodes:
            st.write("Erkannte Barcodes:", barcodes)
        else:
            st.warning("Kein Barcode im Bild erkannt.")

if __name__ == "__main__":
    main()
