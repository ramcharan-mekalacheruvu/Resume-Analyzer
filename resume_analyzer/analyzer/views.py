import json

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ResumeUploadForm
from .models import Resume, ResumeAnalysis

from .services.resume_parser import extract_resume_text
from .services.skill_extractor import extract_skills
from .services.recommender import recommend_jobs
from .services.ats_score import calculate_ats_score


def home(request):
    return render(request, "home.html")


def upload_resume(request):

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save()

            try:

                # 1. Get uploaded file path
                file_path = resume.resume_file.path

                # 2. Extract text
                extracted_text = extract_resume_text(
                    file_path
                )

                resume.extracted_text = extracted_text
                resume.save()

                # 3. Extract skills
                skills = extract_skills(
                    extracted_text
                )

                # 4. Calculate ATS score
                ats_score = calculate_ats_score(
                    extracted_text,
                    skills
                )

                # 5. Recommend suitable jobs
                recommendations = recommend_jobs(
                    extracted_text,
                    skills,
                    top_n=5
                )

                # 6. Save recommendations
                recommended_jobs = []

                for job in recommendations:

                    recommended_jobs.append({
                        "title": job["title"],
                        "description": job["description"],
                        "score": job["score"],
                        "tfidf_score": job["tfidf_score"],
                        "skill_score": job["skill_score"],
                        "matching_skills": job[
                            "matching_skills"
                        ],
                        "missing_skills": job[
                            "missing_skills"
                        ],
                    })

                # 7. Save analysis in database
                ResumeAnalysis.objects.update_or_create(

                    resume=resume,

                    defaults={
                        "ats_score": ats_score,

                        "extracted_skills": ", ".join(
                            skills
                        ),

                        "recommended_jobs":
                            json.dumps(
                                recommended_jobs
                            ),

                        "missing_skills": ", ".join(
                            sorted(
                                {
                                    skill
                                    for job in recommendations
                                    for skill in job[
                                        "missing_skills"
                                    ]
                                }
                            )
                        ),
                    }
                )

                # 8. Redirect to result page
                return redirect(
                    "upload_success",
                    resume_id=resume.id
                )

            except ValueError as error:

                resume.delete()

                form.add_error(
                    "resume_file",
                    str(error)
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

    # Convert JSON string back to Python list
    recommended_jobs = json.loads(
        analysis.recommended_jobs
    )

    return render(
        request,
        "results.html",
        {
            "resume": resume,
            "analysis": analysis,
            "recommended_jobs": recommended_jobs,
        }
    )