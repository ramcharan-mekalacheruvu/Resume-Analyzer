import csv
import os
import re


def load_skills():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )

    csv_path = os.path.join(
        base_dir,
        "datasets",
        "skills.csv"
    )

    skills = []

    with open(
        csv_path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            skill = row.get("skill")

            if skill:
                skills.append(
                    skill.strip()
                )

    return skills


def extract_skills(resume_text):

    if not resume_text:
        return []

    text = resume_text.lower()

    available_skills = load_skills()

    found_skills = []

    for skill in available_skills:

        skill_lower = skill.lower()

        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills