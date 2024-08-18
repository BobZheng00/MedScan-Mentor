import streamlit as st
import os
import sys
import io
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from db.query import *
from db.study import *

from streamlit_drawable_canvas import st_canvas

from PIL import Image

def display(id):
    study = get_one_study(id)
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

display('66c14f704bf922ef708f7e74')