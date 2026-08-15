from pathlib import Path
import pickle

from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "trained_models"

TFIDF_PATH = MODEL_DIR / "tfidf.pkl"


def calculate_similarity(resume_text, job_text):
    """
    Calculate TF-IDF cosine similarity between
    resume text and a job's text.
    """

    # Load trained TF-IDF model
    with open(TFIDF_PATH, "rb") as file:
        tfidf = pickle.load(file)

    # Convert resume and job text into vectors
    vectors = tfidf.transform([
        resume_text,
        job_text
    ])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    # Convert 0-1 to 0-100
    return similarity * 100