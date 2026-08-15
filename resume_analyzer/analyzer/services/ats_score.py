def calculate_ats_score(
    resume_text,
    extracted_skills
):

    score = 0

    # ----------------------------------
    # Skill score
    # ----------------------------------

    if extracted_skills:

        skill_score = min(
            len(extracted_skills) * 5,
            50
        )

        score += skill_score

    # ----------------------------------
    # Resume length
    # ----------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count >= 300:
        score += 20

    elif word_count >= 150:
        score += 15

    elif word_count >= 75:
        score += 10

    # ----------------------------------
    # Important sections
    # ----------------------------------

    important_sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
    ]

    text_lower = resume_text.lower()

    section_count = 0

    for section in important_sections:

        if section in text_lower:
            section_count += 1

    score += section_count * 6

    # Maximum 100

    return min(
        score,
        100
    )