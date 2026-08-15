def generate_ats_feedback(text, skills, score):

    feedback = []

    text_lower = text.lower()

    # Skills
    if len(skills) < 5:
        feedback.append(
            "Add more relevant technical skills."
        )

    elif len(skills) < 10:
        feedback.append(
            "Consider adding more job-related technical skills."
        )

    else:
        feedback.append(
            "Good number of technical skills detected."
        )

    # Projects
    if "project" not in text_lower:
        feedback.append(
            "Add a Projects section to highlight practical experience."
        )

    # Education
    if "education" not in text_lower:
        feedback.append(
            "Add an Education section."
        )

    # Experience
    if (
        "experience" not in text_lower
        and "internship" not in text_lower
    ):
        feedback.append(
            "Consider adding internship or work experience."
        )

    # Contact
    if "@" not in text:
        feedback.append(
            "Add a professional email address."
        )

    # Score-based feedback
    if score >= 80:

        feedback.append(
            "Your resume has a strong ATS-friendly structure."
        )

    elif score >= 60:

        feedback.append(
            "Your resume is reasonably ATS-friendly, "
            "but some areas can be improved."
        )

    else:

        feedback.append(
            "Your resume needs improvement for better ATS compatibility."
        )

    return feedback