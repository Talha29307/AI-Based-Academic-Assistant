from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def chunk_text(text):
    chunks = []

    paragraphs = text.split("\n")

    current_chunk = ""

    for para in paragraphs:
        para = para.strip()

        if len(para) < 40:
            continue

        current_chunk += " " + para

        if len(current_chunk) > 350:
            chunks.append(current_chunk.strip())
            current_chunk = ""

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def retrieve_answer(text, query, top_k=3):
    chunks = chunk_text(text)

    if not chunks:
        return "No useful content found in the uploaded document."

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(chunks + [query])

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    ).flatten()

    ranked = similarities.argsort()[::-1]

    threshold = 0.08

    selected = []

    for idx in ranked:
        if similarities[idx] >= threshold:
            selected.append(chunks[idx])

        if len(selected) == top_k:
            break

    if not selected:
        return "Sorry, I couldn't find relevant information related to your query."

    return "\n\n".join(selected)