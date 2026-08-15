import pickle
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = BASE_DIR / "trained_models"

TFIDF_PATH = MODEL_DIR / "tfidf.pkl"

JOB_VECTORS_PATH = MODEL_DIR / "job_vectors.pkl"


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

def load_model():

    with open(
        TFIDF_PATH,
        "rb"
    ) as file:

        vectorizer = pickle.load(
            file
        )

    with open(
        JOB_VECTORS_PATH,
        "rb"
    ) as file:

        data = pickle.load(
            file
        )

    return (
        vectorizer,
        data["jobs"],
        data["vectors"]
    )


# --------------------------------------------------
# Predict suitable jobs
# --------------------------------------------------

def predict_jobs(
    resume_text,
    top_n=5
):

    vectorizer, jobs, job_vectors = load_model()

    # Convert resume text into TF-IDF vector
    resume_vector = vectorizer.transform(
        [resume_text]
    )

    # Calculate cosine similarity
    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    results = []

    for index, similarity in enumerate(
        similarities
    ):

        job = jobs[index]

        results.append({

            "title": job["job_title"],

            "description": job["description"],

            "skills": job["skills"],

            "similarity": round(
                similarity * 100
            ),

        })

    # Highest similarity first
    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_n]