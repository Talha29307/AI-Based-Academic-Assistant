import streamlit as st
from src.pdf_reader import read_pdf
from src.text_preprocessor import clean_text
from src.retriever import retrieve_answer
from pathlib import Path

st.set_page_config(
    page_title="AI-Based Academic Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI-Based Academic Assistant")

uploaded_file = st.file_uploader(
    "Upload an Academic PDF",
    type="pdf"
)

if uploaded_file is not None:

    save_path = Path("data/pdfs") / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    pdf_text = read_pdf(str(save_path))
    cleaned_text = clean_text(pdf_text)

    query = st.text_input("Ask a question")

    if query:
        answer = retrieve_answer(cleaned_text, query)

        st.subheader("Relevant Content")
        st.success(answer)

    st.text_area(
        "Extracted Text",
        cleaned_text,
        height=400
    )


