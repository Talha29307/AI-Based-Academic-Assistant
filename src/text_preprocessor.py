import re

def clean_text(text):
    """
    Cleans extracted PDF text while preserving paragraph structure.
    """

    # Remove extra spaces/tabs (NOT newlines)
    text = re.sub(r"[ \t]+", " ", text)

    # Remove unwanted characters
    text = re.sub(r"[^\w\s.,;:?!()-]", "", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()