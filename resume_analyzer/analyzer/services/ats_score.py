import re


def calculate_ats_score(text, skills):
    """
    Calculate a simple ATS-style resume score.

    The score is based on:
    - Resume length
    - Number of detected skills
    - Important resume sections
    - Contact information
    """

    score = 0

    text_lower = text.lower()

    # -------------------------------------------------
    # 1. Resume length
    # -------------------------------------------------

    words = re.findall(r"\b\w+\b", text)

    word_count = len(words)

    if word_count >= 300:
        score += 20
    elif word_count >= 150:
        score += 15
    elif word_count >= 75:
        score += 10
    else:
        score += 5

    # -------------------------------------------------
    # 2. Technical skills
    # -------------------------------------------------

    skill_count = len(skills)

    if skill_count >= 12:
        score += 25
    elif skill_count >= 8:
        score += 20
    elif skill_count >= 5:
        score += 15
    elif skill_count >= 3:
        score += 10
    else:
        score += 5

    # -------------------------------------------------
    # 3. Resume sections
    # -------------------------------------------------

    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
    ]

    section_count = 0

    for section in sections:

        if section in text_lower:
            section_count += 1

    score += section_count * 5

    # -------------------------------------------------
    # 4. Email
    # -------------------------------------------------

    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

    if re.search(email_pattern, text):
        score += 5

    # -------------------------------------------------
    # 5. Phone number
    # -------------------------------------------------

    phone_pattern = r"\+?\d[\d\s\-]{8,}\d"

    if re.search(phone_pattern, text):
        score += 5

    # -------------------------------------------------
    # 6. Action words
    # -------------------------------------------------

    action_words = [
        "developed",
        "built",
        "created",
        "designed",
        "implemented",
        "developed",
        "managed",
        "integrated",
        "deployed",
        "analyzed",
    ]

    action_count = sum(
        1
        for word in action_words
        if word in text_lower
    )

    if action_count >= 5:
        score += 15
    elif action_count >= 3:
        score += 10
    elif action_count >= 1:
        score += 5

    # -------------------------------------------------
    # Limit score to 100
    # -------------------------------------------------

    return min(score, 100)