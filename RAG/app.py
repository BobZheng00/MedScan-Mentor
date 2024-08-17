import streamlit as st
from rag import fetch_articles, simulate_rag_pipeline


def main():
    st.title("Brain Disease Analysis & Literature Retrieval")

    # User inputs
    disease_type = st.text_input("Enter the type of brain disease (e.g., Glioma, Meningioma):")
    user_input_bbox = st.text_input("Enter your bounding box coordinates (e.g., 100,150,200,250):")
    correct_bbox = st.text_input("Enter the correct bounding box coordinates (e.g., 102,148,198,252):")
    user_interpretation = st.text_area("Enter your interpretation of the disease:")

    if st.button("Analyze"):
        if disease_type and user_input_bbox and correct_bbox and user_interpretation:
            # Clean and convert bounding box inputs to lists of integers
            try:
                user_input_bbox = list(
                    map(int, user_input_bbox.replace('(', '').replace(')', '').replace(' ', '').split(',')))
                correct_bbox = list(
                    map(int, correct_bbox.replace('(', '').replace(')', '').replace(' ', '').split(',')))

                # Simulate RAG pipeline processing
                output = simulate_rag_pipeline(user_input_bbox, correct_bbox, user_interpretation, disease_type)
                st.write("### MedScan Analysis Report:")
                st.write(output)
            except ValueError:
                st.write("Please enter valid bounding box coordinates.")
        else:
            st.write("Please provide all inputs to perform the analysis.")


if __name__ == "__main__":
    main()
