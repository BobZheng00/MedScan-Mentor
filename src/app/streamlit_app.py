from PIL import Image
import streamlit as st
import torch
import numpy as np
from streamlit_drawable_canvas import st_canvas

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