import csv
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_PATH = BASE_DIR / "datasets" / "jobs.csv"

MODEL_DIR = BASE_DIR / "trained_models"

TFIDF_PATH = MODEL_DIR / "tfidf.pkl"

JOB_VECTORS_PATH = MODEL_DIR / "job_vectors.pkl"


# --------------------------------------------------
# Load jobs
# --------------------------------------------------

def load_jobs():

    jobs = []

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Combine description and skills
            job_text = (
                row["description"]
                + " "
                + row["skills"].replace("|", " ")
            )

            jobs.append({
                "job_title": row["job_title"],
                "description": row["description"],
                "skills": row["skills"],
                "text": job_text,
            })

    return jobs


# --------------------------------------------------
# Train TF-IDF
# --------------------------------------------------

def train_model():

    print("Loading job dataset...")

    jobs = load_jobs()

    job_texts = [
        job["text"]
        for job in jobs
    ]

    print(
        f"Loaded {len(jobs)} jobs."
    )

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    # Convert job descriptions to vectors
    job_vectors = vectorizer.fit_transform(
        job_texts
    )

    # Create trained_models directory
    MODEL_DIR.mkdir(
        exist_ok=True
    )

    # Save vectorizer
    with open(
        TFIDF_PATH,
        "wb"
    ) as file:

        pickle.dump(
            vectorizer,
            file
        )

    # Save job information + vectors
    with open(
        JOB_VECTORS_PATH,
        "wb"
    ) as file:

        pickle.dump(
            {
                "jobs": jobs,
                "vectors": job_vectors,
            },
            file
        )

    print()
    print("TF-IDF model trained successfully.")
    print(
        f"Saved: {TFIDF_PATH}"
    )
    print(
        f"Saved: {JOB_VECTORS_PATH}"
    )


if __name__ == "__main__":

    train_model()