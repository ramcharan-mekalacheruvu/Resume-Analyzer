import csv
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


BASE_DIR = Path(__file__).resolve().parents[2]

JOBS_FILE = BASE_DIR / "datasets" / "jobs.csv"

MODEL_DIR = BASE_DIR / "trained_models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


print("Loading job dataset...")

jobs = []

with open(
    JOBS_FILE,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        jobs.append({
            "title": row["job_title"],
            "description": row["description"],
            "skills": row["skills"],
        })


print(f"Loaded {len(jobs)} jobs.")


job_texts = []

for job in jobs:

    text = (
        job["title"]
        + " "
        + job["description"]
        + " "
        + job["skills"].replace("|", " ")
    )

    job_texts.append(text)


vectorizer = TfidfVectorizer(
    stop_words="english"
)

job_vectors = vectorizer.fit_transform(
    job_texts
)


with open(
    MODEL_DIR / "tfidf.pkl",
    "wb"
) as file:

    pickle.dump(
        vectorizer,
        file
    )


with open(
    MODEL_DIR / "job_vectors.pkl",
    "wb"
) as file:

    pickle.dump(
        job_vectors,
        file
    )


print("TF-IDF model trained successfully.")

print(
    f"Saved: {MODEL_DIR / 'tfidf.pkl'}"
)

print(
    f"Saved: {MODEL_DIR / 'job_vectors.pkl'}"
)