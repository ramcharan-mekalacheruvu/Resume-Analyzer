import csv
from pathlib import Path

from .similarity import calculate_similarity


BASE_DIR = Path(__file__).resolve().parents[2]

JOBS_FILE = (
    BASE_DIR / "datasets" / "jobs.csv"
)


def load_jobs():

    jobs = []

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            skills = [
                skill.strip().lower()
                for skill in row["skills"].split("|")
            ]

            jobs.append({
                "title": row["job_title"],
                "description": row["description"],
                "skills": skills,
            })

    return jobs


def recommend_jobs(
    resume_text,
    resume_skills,
    top_n=5
):

    jobs = load_jobs()

    resume_skills = {
        skill.lower()
        for skill in resume_skills
    }

    results = []

    for job in jobs:

        job_skills = set(
            job["skills"]
        )

        # -----------------------------------------
        # Skill matching
        # -----------------------------------------

        matching_skills = (
            resume_skills & job_skills
        )

        missing_skills = (
            job_skills - resume_skills
        )

        if job_skills:

            skill_score = (
                len(matching_skills)
                / len(job_skills)
            ) * 100

        else:

            skill_score = 0

        # -----------------------------------------
        # TF-IDF similarity
        # -----------------------------------------

        tfidf_score = calculate_similarity(
            resume_text,
            " ".join(job["skills"])
        )

        # -----------------------------------------
        # Final score
        # -----------------------------------------

        final_score = (
            0.60 * skill_score
            +
            0.40 * tfidf_score
        )

        results.append({

            "title": job["title"],

            "description":
                job["description"],

            "score": round(
                final_score
            ),

            "tfidf_score": round(
                tfidf_score
            ),

            "skill_score": round(
                skill_score
            ),

            "matching_skills":
                sorted(matching_skills),

            "missing_skills":
                sorted(missing_skills),

        })

    # Highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_n]