from PIL import Image
import streamlit as st
import torch
import numpy as np
from streamlit_drawable_canvas import st_canvas

import os
import io
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from RAG.rag import simulate_rag_pipeline

from db.study import *
from db.query import *

username = 'guest'

def get_image_byte_array(results):
    # get image instance
    img = Image.fromarray(np.squeeze(results.render()))
    
    # turn image to byte array
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    
    return img_byte_array

def display_studies(username):
    study = get_all_study(username)
    study_id = study['_id']
    study_type = study['type']
    st.selectbox("Select a study:", [study], format_func=lambda x: f"{study_type} tumor detection - Study ID: {study_id}")
    if st.button('Display Study'):
        st.session_state["id"] = study_id
        st.rerun()

def display_study(id):
    study = get_one_study(id)
    st.markdown(
        """
        <style>
        /* Adjust the main content area to be wider */
        .block-container {
            max-width: 65%;  /* Adjust this value to control the width */
            padding-left: 1rem;
            padding-right: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1, 1])
    if study != None:
        cord = study['cord']
        initial_rect = {
            "objects": [
                {
                    "type": "rect",
                    "left": str(cord[0]),
                    "top": str(cord[1]),
                    "width": str(int(cord[2]) - int(cord[0])),
                    "height": str(int(cord[3]) - int(cord[1])),
                    "stroke": "#000000",  # Change as needed
                    "strokeWidth": 2,
                    "fill": "rgba(255, 165, 0, 0.3)"
                }
            ]
        }
        target_image = io.BytesIO(study['target'])
        image = Image.open(target_image)
        with col1:
            # st.image(study['target'], caption="Model Prediction", use_column_width=True)
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # Set fill color with transparency
                stroke_width=2,
                background_image=image,
                update_streamlit=True,
                height=image.height,
                width=image.width,
                drawing_mode="rect",  # Restrict to rectangle drawing
                key="canvas",
                initial_drawing=initial_rect
            )
        with col2:
            st.image(study['correct'], caption="Model Prediction", use_column_width=True)
        
        st.write(study['analysis'])

if __name__ == "__main__":
    def load_model():
        inference_model = torch.hub.load(
            'ultralytics/yolov5', 'custom',
            path='results/brain_tumor_detector/weights/best.pt'
        )
        return inference_model

    model = load_model()

    def run_inference(image):
        results = model(image)
        return results


    st.title("MedScan Mentor - Tumor Detection and Feedback")

    st.markdown(
        """
        <style>
        /* Adjust the main content area to be wider */
        .block-container {
            max-width: 65%;  /* Adjust this value to control the width */
            padding-left: 1rem;
            padding-right: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    user_input_bbox = []
    mode = st.sidebar.radio('Select Page:', ['Upload', 'Previous Analysis'])

    if mode == 'Upload':
        # Upload CT Scan Image
        uploaded_file = st.file_uploader("Upload a CT scan image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            with col1:
                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Set fill color with transparency
                    stroke_width=2,
                    background_image=image,
                    update_streamlit=True,
                    height=image.height,
                    width=image.width,
                    drawing_mode="rect",  # Restrict to rectangle drawing
                    key="canvas",
                )

            # Retrieve the coordinates of the drawn rectangle
            if canvas_result.json_data is not None:
                objects = canvas_result.json_data["objects"]
                if len(objects) > 0:
                    for obj in objects:
                        left = obj["left"]
                        top = obj["top"]
                        width = obj["width"]
                        height = obj["height"]

                        # Convert to bounding box format (xmin, ymin, xmax, ymax)
                        xmin, ymin = left, top
                        xmax, ymax = left + width, top + height
                        user_input_bbox = [xmin, ymin, xmax, ymax]
                        st.write(f"Bounding box: (xmin: {xmin}, ymin: {ymin}, xmax: {xmax}, ymax: {ymax})")

            # Run YOLO model on the uploaded image
            results = run_inference(image)
            print(results.pandas().xyxy[0])

            # Interpret results
            # pred_class = results.pandas().xyxy[0]['name'][0] if len(results.pandas().xyxy[0]) > 0 else 'no_tumor'
            # if pred_class == 'glioma':
            #     st.write("The model detected a glioma tumor in the CT scan.")
            # else:
            #     st.write("The model did not detect any tumor in the CT scan.")

            # Student Interpretation
            st.write("### Your Interpretation")
            student_interpretation = st.text_area("Enter your interpretation of the CT scan")

            # Feedback based on model prediction
            if st.button("Get Feedback"):
                # Display YOLOv5 results
                with col2:
                    st.image(np.squeeze(results.render()), caption="Model Prediction", use_column_width=True)

                # Simulate RAG pipeline processing
                if user_input_bbox:
                    summary = simulate_rag_pipeline(user_input_bbox,
                                          [results.pandas().xyxy[0]["xmin"][0],
                                           results.pandas().xyxy[0]["ymin"][0],
                                           results.pandas().xyxy[0]["xmax"][0],
                                           results.pandas().xyxy[0]["ymax"][0]],
                                          student_interpretation,
                                          results.pandas().xyxy[0]["name"][0]
                                          )
                    st.write(summary)

                    correct_byte_array = get_image_byte_array(results)

                    study = Study(uploaded_file.getvalue(), [xmin, ymin, xmax, ymax], correct_byte_array, student_interpretation, summary, 'Brain', username)

                    add_study(username, study)
    else:
        if "id" in st.session_state and st.session_state["id"]:
            display_study(st.session_state["id"])
        else:
            display_studies('guest')