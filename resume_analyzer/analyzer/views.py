import json

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ResumeUploadForm
from .models import Resume, ResumeAnalysis

from .services.resume_parser import extract_resume_text
from .services.skill_extractor import extract_skills
from .services.recommender import recommend_jobs


def home(request):
    return render(request, "home.html")


def generate_ats_feedback(score, skills, resume_text):
    feedback = []

    if score >= 80:
        feedback.append(
            "Your resume has a strong ATS compatibility score."
        )
    elif score >= 60:
        feedback.append(
            "Your resume has good ATS compatibility, but there is room for improvement."
        )
    else:
        feedback.append(
            "Your resume needs improvement to achieve better ATS compatibility."
        )

    if len(skills) < 8:
        feedback.append(
            "Add more relevant technical skills that match your target job roles."
        )

    text_lower = resume_text.lower()

    if "experience" not in text_lower:
        feedback.append(
            "Consider adding an Experience or Internship section."
        )

    if "project" not in text_lower:
        feedback.append(
            "Add detailed academic or personal projects with technologies used."
        )

    if "certification" not in text_lower:
        feedback.append(
            "Add relevant certifications to strengthen your profile."
        )

    if len(resume_text) < 1500:
        feedback.append(
            "Your resume content appears short. Add more measurable project and experience details."
        )

    feedback.append(
        "Use clear section headings such as Education, Skills, Projects, Experience and Certifications."
    )

    feedback.append(
        "Use job-specific keywords naturally throughout the resume."
    )

    return feedback


def calculate_ats_score(resume_text, skills):

    score = 0

    # Skill coverage
    if len(skills) >= 10:
        score += 30
    elif len(skills) >= 7:
        score += 25
    elif len(skills) >= 4:
        score += 18
    elif len(skills) >= 1:
        score += 10

    text = resume_text.lower()

    # Resume sections
    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications",
    ]

    section_score = 0

    for section in sections:
        if section in text:
            section_score += 8

    score += min(section_score, 40)

    # Resume length/content
    if len(resume_text) >= 2000:
        score += 20
    elif len(resume_text) >= 1000:
        score += 15
    elif len(resume_text) >= 500:
        score += 10

    return min(score, 100)


def upload_resume(request):

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save()

            try:

                # --------------------------------
                # Extract resume text
                # --------------------------------

                file_path = resume.resume_file.path

                extracted_text = extract_resume_text(
                    file_path
                )

                resume.extracted_text = extracted_text
                resume.save()

                # --------------------------------
                # Extract skills
                # --------------------------------

                skills = extract_skills(
                    extracted_text
                )

                # Make sure skills is a list
                if not skills:
                    skills = []

                # --------------------------------
                # Calculate ATS score
                # --------------------------------

                ats_score = calculate_ats_score(
                    extracted_text,
                    skills
                )

                # --------------------------------
                # Generate ATS feedback
                # --------------------------------

                ats_feedback = generate_ats_feedback(
                    ats_score,
                    skills,
                    extracted_text
                )

                # --------------------------------
                # Recommend jobs
                # --------------------------------

                job_results = recommend_jobs(
                    extracted_text,
                    skills,
                    top_n=5
                )

                # --------------------------------
                # Find missing skills
                # --------------------------------

                missing_skills = set()

                for job in job_results:

                    for skill in job.get(
                        "missing_skills",
                        []
                    ):
                        missing_skills.add(
                            skill
                        )

                # --------------------------------
                # Save complete analysis
                # --------------------------------

                ResumeAnalysis.objects.update_or_create(

                    resume=resume,

                    defaults={
                        "ats_score": ats_score,

                        "ats_feedback": json.dumps(
                            ats_feedback
                        ),

                        "extracted_skills": json.dumps(
                            skills
                        ),

                        "recommended_jobs": json.dumps(
                            job_results
                        ),

                        "missing_skills": json.dumps(
                            sorted(missing_skills)
                        ),
                    }
                )

                return redirect(
                    "upload_success",
                    resume_id=resume.id
                )

            except Exception as error:

                resume.delete()

                form.add_error(
                    "resume_file",
                    f"Analysis failed: {error}"
                )

    else:

        form = ResumeUploadForm()

    return render(
        request,
        "upload.html",
        {
            "form": form
        }
    )


def upload_success(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id
    )

    analysis = get_object_or_404(
        ResumeAnalysis,
        resume=resume
    )

    skills = json.loads(
        analysis.extracted_skills or "[]"
    )

    jobs = json.loads(
        analysis.recommended_jobs or "[]"
    )

    missing_skills = json.loads(
        analysis.missing_skills or "[]"
    )

    feedback = json.loads(
        analysis.ats_feedback or "[]"
    )

    return render(
        request,
        "results.html",
        {
            "resume": resume,
            "analysis": analysis,
            "skills": skills,
            "skill_count": len(skills),
            "jobs": jobs,
            "job_count": len(jobs),
            "missing_skills": missing_skills,
            "feedback": feedback,
        }
    )