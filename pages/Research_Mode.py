import sys
import os
import tempfile
import re

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
st.caption(
    "Upload a research idea, project report, or physics paper and get a Feynman-style critique."
)

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

                try:
                    clarity = re.search(
                        r"Clarity:\s*(\d+)/10",
                        review
                    ).group(1)

                    rigor = re.search(
                        r"Scientific Rigor:\s*(\d+)/10",
                        review
                    ).group(1)

                    evidence = re.search(
                        r"Evidence Strength:\s*(\d+)/10",
                        review
                    ).group(1)

                    experiment = re.search(
                        r"Experimental Design:\s*(\d+)/10",
                        review
                    ).group(1)

                    simplicity = re.search(
                        r"Simplicity:\s*(\d+)/10",
                        review
                    ).group(1)

                    overall = re.search(
                        r"Overall Feynman Score:\s*(\d+)/10",
                        review
                    ).group(1)

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Clarity",
                        f"{clarity}/10"
                    )

                    col2.metric(
                        "Scientific Rigor",
                        f"{rigor}/10"
                    )

                    col3.metric(
                        "Evidence Strength",
                        f"{evidence}/10"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Experimental Design",
                        f"{experiment}/10"
                    )

                    col2.metric(
                        "Simplicity",
                        f"{simplicity}/10"
                    )

                    col3.metric(
                        "Feynman Score",
                        f"{overall}/10"
                    )

                    score = int(overall)

                    if score >= 8:
                        st.success(
                            "🟢 Strong Research Direction"
                        )

                    elif score >= 6:
                        st.info(
                            "🔵 Promising but Needs Validation"
                        )

                    elif score >= 4:
                        st.warning(
                            "🟡 Interesting Idea, Weak Evidence"
                        )

                    else:
                        st.error(
                            "🔴 Major Scientific Gaps"
                        )

                except Exception:
                    st.info(
                        "Scorecard could not be parsed automatically, showing full review below."
                    )

                clean_review = review

                if "## Core Idea" in review:

                    clean_review = (
                        "## Core Idea"
                        + review.split(
                            "## Core Idea",
                            1
                        )[1]
                    )

                st.markdown(
                    clean_review
                )

    except Exception as e:
        st.error(
            f"Could not process file: {e}"
        )