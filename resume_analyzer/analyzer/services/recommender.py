from analyzer.ml.predict import predict_jobs


def recommend_jobs(
    resume_text,
    extracted_skills,
    top_n=5
):
    """
    Recommend suitable jobs using:

    60% TF-IDF similarity
    40% skill matching
    """

    # Get TF-IDF recommendations
    tfidf_results = predict_jobs(
        resume_text,
        top_n=10
    )

    # Convert resume skills to lowercase
    resume_skills = {
        skill.lower().strip()
        for skill in extracted_skills
    }

    final_results = []

    for job in tfidf_results:

        # Convert required skills to lowercase
        required_skills = {
            skill.lower().strip()
            for skill in job["skills"].split("|")
        }

        # Find matching skills
        matching_skills = (
            resume_skills
            & required_skills
        )

        # Find missing skills
        missing_skills = (
            required_skills
            - resume_skills
        )

        # Calculate skill match percentage
        if required_skills:

            skill_score = (
                len(matching_skills)
                / len(required_skills)
            ) * 100

        else:

            skill_score = 0

        # TF-IDF score
        tfidf_score = job["similarity"]

        # Final weighted score
        final_score = (
            (tfidf_score * 0.60)
            + (skill_score * 0.40)
        )

        final_results.append({

            "title": job["title"],

            "description": job["description"],

            "score": round(
                final_score
            ),

            "tfidf_score": round(
                tfidf_score
            ),

            "skill_score": round(
                skill_score
            ),

            "matching_skills": sorted(
                matching_skills
            ),

            "missing_skills": sorted(
                missing_skills
            ),

        })

    # Sort by final score
    final_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return final_results[:top_n]