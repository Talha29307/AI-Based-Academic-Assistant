import streamlit as st
from pathlib import Path

from src.pdf_reader import read_pdf
from src.text_preprocessor import clean_text
from src.retriever import retrieve_answer

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI-Based Academic Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.title("📚 Project Info")

    st.markdown("""
### Features

✅ PDF Upload

✅ NLP Preprocessing

✅ TF-IDF Retrieval

✅ Cosine Similarity

✅ Context-Based Answers
""")

    st.divider()

    st.markdown("""
### Tech Stack

- Python
- Streamlit
- Scikit-learn
- PyPDF
- NLP
""")

    st.divider()

    st.markdown("""
### 💡 Tips

- Upload a clear academic PDF.
- Ask specific questions.
- Use keywords from the document.
""")

# ----------------------------------------------------
# Main Title
# ----------------------------------------------------

st.title("📚 AI-Based Academic Assistant")

st.caption("Upload • Ask • Retrieve • Learn")

st.markdown("""
#### 🎓 Intelligent Academic Question Answering

Upload an academic PDF and receive context-aware answers using **TF-IDF**, **Cosine Similarity**, and **NLP preprocessing**.
""")

# ----------------------------------------------------
# Upload PDF
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload an Academic PDF",
    type="pdf"
)

if uploaded_file is None:

    st.info("👆 Upload an academic PDF to begin.")

else:

    st.info(f"📄 Uploaded PDF: {uploaded_file.name}")

    save_path = Path("data/pdfs") / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("📖 Reading and processing PDF..."):

        pdf_text = read_pdf(str(save_path))
        cleaned_text = clean_text(pdf_text)

    st.divider()

    # ------------------------------------------------
    # Question Section
    # ------------------------------------------------

    st.subheader("❓ Ask Your Question")

col1, col2 = st.columns([4.5,1.2])

with col1:
    query = st.text_input(
        "",
        placeholder="Example: What is a social institution?",
        label_visibility="collapsed"
    )

with col2:
    ask = st.button("🚀 Ask", use_container_width=True)

if ask:

    if not query.strip():
        st.warning("⚠️ Please enter a question.")

    else:

        with st.spinner("🤖 Searching the document..."):

            answer = retrieve_answer(cleaned_text, query)

        st.divider()

        st.subheader("🤖 AI Assistant Response")

        if answer.startswith("⚠️"):
            st.warning(answer)
        else:
            st.success(answer)

    # ------------------------------------------------
    # Advanced Options
    # ------------------------------------------------

    with st.expander("⚙️ Advanced Options"):

        st.text_area(
            "Extracted Text",
            cleaned_text,
            height=350
        )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.caption(
    "Developed by Talha Ahmad | AI-Based Academic Assistant using Retrieval-Augmented Techniques | NTCC Project 2026"
)