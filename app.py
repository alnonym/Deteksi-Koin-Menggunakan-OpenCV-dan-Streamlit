import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Deteksi Koin")
st.write("Upload gambar koin, lalu sistem akan mendeteksi dan menghitung jumlahnya.")

uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    output = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((3,3), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    clean = cv2.medianBlur(clean, 5)

    contours, _ = cv2.findContours(
        clean,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    coin_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(output, (x,y), (x+w,y+h), (0,255,0), 2)
            coin_count += 1

    st.image(image, caption="Gambar Asli", use_container_width=True)
    st.image(thresh, caption="Threshold Awal", use_container_width=True)
    st.image(clean, caption="Threshold Bersih", use_container_width=True)
    st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB),
             caption=f"Hasil Deteksi ({coin_count} koin)",
             use_container_width=True)

    st.success(f"Jumlah koin terdeteksi: {coin_count}")