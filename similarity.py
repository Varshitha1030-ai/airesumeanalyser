"""Resume <-> job description similarity.

Default: TF-IDF + cosine similarity (light, deploys anywhere).
Optional: sentence-transformers 'all-MiniLM-L6-v2' if the package is installed.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_model = None


def semantic_available() -> bool:
    try:
        import sentence_transformers  # noqa: F401
        return True
    except ImportError:
        return False


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def tfidf_similarity(resume: str, job: str) -> float:
    if not resume.strip() or not job.strip():
        return 0.0
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vec.fit_transform([resume, job])
    except ValueError:  # nothing left after stop-word removal
        return 0.0
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def semantic_similarity(resume: str, job: str) -> float:
    model = _get_model()
    emb = model.encode([resume, job])
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])


def similarity_percent(resume: str, job: str, use_semantic: bool = False) -> float:
    """Return similarity as a 0-100 percentage."""
    if use_semantic and semantic_available():
        score = semantic_similarity(resume, job)
    else:
        score = tfidf_similarity(resume, job)
    return round(max(score, 0.0) * 100, 1)
