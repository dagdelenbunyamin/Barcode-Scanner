import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

def decode_barcode(image):
    barcodes = decode(image)
    if barcodes:
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            return barcode_data
    return None

def main():
    st.title("Barcode-Scanner mit Bild-Upload")

    uploaded_file = st.file_uploader("Wähle ein Bild mit Barcode", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image.convert('RGB'))  # Bild in RGB umwandeln, falls es in einem anderen Format vorliegt

        barcode_data = decode_barcode(image)

        if barcode_data:
            st.success(f"Barcode erkannt: {barcode_data}")
        else:
            st.error("Kein Barcode erkannt. Bitte versuche ein anderes Bild.")

if __name__ == "__main__":
    main()
