# -*- coding: utf-8 -*-
"""Deteksi_Rempah_App.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1icxpPFxkpyksk2CV6RYiPfHTzVUMctbk
"""

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import os
import gdown
import matplotlib.pyplot as plt
import seaborn as sns

# URL Google Drive file model (gunakan URL unduhan langsung)
MODEL_URL = "https://drive.google.com/uc?export=download&id=1Ta_Uz9zgL7FSsK3bdFQnAO9_ZJ61QGRT"
MODEL_PATH = "chili_leaf_disease.h5"

# Fungsi untuk mengunduh model jika belum ada
def download_model():
    if not os.path.exists(MODEL_PATH):
        st.info("Mengunduh model dari Google Drive. Harap tunggu...")
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# Fungsi untuk memuat model
@st.cache_resource
def load_model():
    download_model() 
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

# Fungsi untuk memproses gambar
def preprocess_image(image, target_size=(224, 224)):
    image = image.resize(target_size)  # Ubah ukuran gambar ke 224x224 (sesuai dengan input model)
    image = np.array(image) / 255.0   # Normalisasi pixel (0-1)
    image = np.expand_dims(image, axis=0)  # Tambahkan batch dimension
    return image

# Fungsi untuk prediksi
def predict_image(model, image):
    predictions = model.predict(image)
    return predictions

# Daftar nama kelas (sesuaikan dengan dataset Anda)
class_names = ["Sehat", "Daun Keriting", "Bercak Daun", "Kutu Kebul", "Kekuningan"] 

# Mulai aplikasi Streamlit
st.title("Aplikasi Deteksi Penyakit Pada Daun Tanaman Cabai🌶️")
st.write("Unggah gambar daun cabai untuk mendeteksi apakah daun tersebut sehat atau memiliki penyakit.")

# Upload gambar
uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)  # Buka gambar dengan PIL
    st.image(image, caption="Unggah Gambar Daun Cabai", width=500)  # Tampilkan gambar dengan lebar sesuai kolom

    # Proses dan prediksi
    model = load_model()  # Muat model
    processed_image = preprocess_image(image)  # Proses gambar
    predictions = predict_image(model, processed_image)  # Prediksi

    # Temukan kelas dengan prediksi tertinggi
    class_idx = np.argmax(predictions)
    confidence = predictions[0][class_idx]

    # Tampilkan hasil prediksi
    st.write(f"**🔍Deteksi Penyakit:** {class_names[class_idx]}")
    st.write(f"**🌟Kepercayaan Prediksi:** {confidence * 100:.2f}%")

    # Buat diagram persentase prediksi untuk semua kelas
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=class_names, y=predictions[0], ax=ax, palette='viridis')
    ax.set_xticklabels(class_names, rotation=90, fontsize=10)
    ax.set_ylabel("🌟Kepercayaan (%)", fontsize=12)
    ax.set_title("📊Prediksi Kepercayaan Setiap Kelas Rempah", fontsize=14)
    st.pyplot(fig)
