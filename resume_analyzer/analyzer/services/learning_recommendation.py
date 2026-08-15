def get_skills_to_learn(recommendations):

    skill_frequency = {}

    for job in recommendations:

        for skill in job["missing_skills"]:

            skill_frequency[skill] = (
                skill_frequency.get(skill, 0) + 1
            )

    sorted_skills = sorted(
        skill_frequency.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        skill
        for skill, count in sorted_skills[:10]
    ]