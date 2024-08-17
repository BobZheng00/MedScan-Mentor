from predict.predict import detect
from PIL import Image
import streamlit as st
import os

# Streamlit app


def app():
    st.title("Brain Tumor Detector")
    st.write("This app detects brain tumors in CT scans.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded a CT scan.", use_column_width=True)
        st.write("")
        st.write("Classifying...")
        image_name = uploaded_file.name
        image_path = os.path.join("images", image_name)
        with open(image_path, "wb") as file:
            file.write(uploaded_file.getbuffer())
        byte_array = detect(image_name, image_path, "brain")
        st.image(byte_array, caption="Detected Tumors.", use_column_width=True)
        os.remove(image_path)

