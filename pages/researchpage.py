import sys
import os
import tempfile

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from research.analyzer import ResearchAnalyzer
from utils.file_loader import FileLoader


st.set_page_config(
    page_title="Feynman Research Mentor",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Feynman Research Mentor")
st.caption("Upload a research idea, project report, or physics paper and get a Feynman-style critique.")

analyzer = ResearchAnalyzer()

uploaded_file = st.file_uploader(
    "Upload your research/project file",
    type=["pdf", "txt"]
)

max_words = st.slider(
    "Review Length",
    min_value=300,
    max_value=1000,
    value=600,
    step=100
)

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        project_text = FileLoader.load_document(temp_path)

        with st.expander("Preview Extracted Text"):
            st.write(project_text[:3000])

        if st.button("Analyze with Feynman"):

            with st.spinner("Feynman is reviewing your work..."):

                review = analyzer.analyze_project(
                    project_text=project_text[:12000],
                    max_words=max_words
                )

                st.subheader("Richard Feynman's Review")
                st.markdown(review)

    except Exception as e:
        st.error(f"Could not process file: {e}")