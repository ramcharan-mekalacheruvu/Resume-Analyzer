def calculate_ats_score(
    resume_text,
    skills
):

    text = resume_text.lower()

    score = 0

    # -----------------------------------
    # Skill score
    # -----------------------------------

    skill_count = len(skills)

    if skill_count >= 15:
        score += 40

    elif skill_count >= 10:
        score += 35

    elif skill_count >= 7:
        score += 30

    elif skill_count >= 5:
        score += 25

    elif skill_count >= 3:
        score += 20

    else:
        score += 10


    # -----------------------------------
    # Resume sections
    # -----------------------------------

    sections = {

        "education":
            "education" in text,

        "experience":
            "experience" in text
            or "internship" in text,

        "projects":
            "project" in text
            or "projects" in text,

        "certifications":
            "certification" in text
            or "certifications" in text,

        "skills":
            "skills" in text
            or "technical skills" in text,

    }


    section_count = sum(
        sections.values()
    )


    score += section_count * 7


    # -----------------------------------
    # Contact information
    # -----------------------------------

    if "@" in text:
        score += 5

    if "+" in text:
        score += 5


    # -----------------------------------
    # Resume length
    # -----------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count >= 300:
        score += 10

    elif word_count >= 150:
        score += 7

    elif word_count >= 80:
        score += 4


    # -----------------------------------
    # Maximum score
    # -----------------------------------

    score = min(
        score,
        100
    )


    # -----------------------------------
    # Feedback
    # -----------------------------------

    feedback = []

    if skill_count < 5:

        feedback.append(
            "Add more relevant technical skills."
        )

    if not sections["experience"]:

        feedback.append(
            "Consider adding internship or work experience."
        )

    if not sections["projects"]:

        feedback.append(
            "Add academic or personal projects."
        )

    if not sections["certifications"]:

        feedback.append(
            "Add relevant certifications."
        )

    if section_count >= 4:

        feedback.append(
            "Your resume has a good overall structure."
        )


    if not feedback:

        feedback.append(
            "Your resume has a reasonable ATS structure."
        )


    # -----------------------------------
    # Missing skills
    # -----------------------------------

    recommended_basic_skills = [

        "python",
        "java",
        "sql",
        "git",
        "rest api",
        "html",
        "css",
        "javascript",

    ]


    missing_skills = []

    for skill in recommended_basic_skills:

        if skill not in [
            s.lower()
            for s in skills
        ]:

            missing_skills.append(
                skill
            )


    return {

        "score": score,

        "feedback":
            " ".join(feedback),

        "missing_skills":
            missing_skills[:5],

    }