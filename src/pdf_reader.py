import re
from pypdf import PdfReader


def clean_text(text):
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace 3 or more newlines with two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing spaces on each line
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines)


def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            full_text += page_text + "\n"

    return clean_text(full_text)