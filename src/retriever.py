import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def chunk_text(text, max_chunk_size=600):
    """
    Split the document into meaningful chunks by combining
    paragraphs until the chunk reaches the desired size.
    """

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks = []
    current_chunk = ""

    for para in paragraphs:

        if len(current_chunk) + len(para) <= max_chunk_size:
            current_chunk += " " + para
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def extract_context_answer(chunk, max_sentences=3):
    """
    Returns the first few connected sentences from the best chunk.
    This preserves context and makes answers more natural.
    """

    sentences = re.split(r'(?<=[.!?])\s+', chunk)

    relevant_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 20:
            relevant_sentences.append(sentence)

        if len(relevant_sentences) >= max_sentences:
            break

    return "\n\n".join(relevant_sentences)

def retrieve_answer(text, query, top_k=3, threshold=0.10):
    """
    Retrieve the most relevant answer for the user's query.
    """

    chunks = chunk_text(text)

    if not chunks:
        return "No useful content found in the uploaded document."

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(chunks + [query])

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    ).flatten()

    ranked_indices = similarities.argsort()[::-1]

    selected_chunks = []

    for idx in ranked_indices:

        if similarities[idx] < threshold:
            continue

        chunk = chunks[idx]

        if chunk not in selected_chunks:
            selected_chunks.append(chunk)

        if len(selected_chunks) >= top_k:
            break

    if not selected_chunks:
      return (
         "⚠️ No relevant information was found in the uploaded document.\n\n"
         "Suggestions:\n"
         "• Try using different keywords.\n"
         "• Ask a more specific question.\n"
         "• Check if the uploaded PDF contains the requested topic."
    )

    # Dynamic number of sentences based on question type
    query_lower = query.lower()

    if query_lower.startswith(("what", "define")):
       max_sentences = 2
    elif query_lower.startswith(("explain", "describe", "discuss", "how", "why")):
       max_sentences = 4
    else:
       max_sentences = 3

    best_chunk = selected_chunks[0]

    return extract_context_answer(
       best_chunk,
       max_sentences=max_sentences
)