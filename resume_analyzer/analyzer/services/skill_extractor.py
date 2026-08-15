import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

SKILLS_FILE = (
    BASE_DIR / "datasets" / "skills.csv"
)


def load_skills():

    skills = []

    with open(
        SKILLS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            skill = row["skill"].strip()

            if skill:
                skills.append(skill)

    return skills


def extract_skills(text):

    text = text.lower()

    all_skills = load_skills()

    detected = []

    for skill in all_skills:

        skill_lower = skill.lower()

        if skill_lower in text:

            detected.append(
                skill
            )

    return detected