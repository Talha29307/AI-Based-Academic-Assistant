from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def chunk_text(text):
    chunks = []

    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()

        if len(paragraph) > 100:
            chunks.append(paragraph)

    return chunks


def retrieve_answer(text, query):
    chunks = chunk_text(text)

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(chunks + [query])

    similarity = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )

    best_match = similarity.argmax()

    return chunks[best_match]