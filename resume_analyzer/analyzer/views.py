from django.shortcuts import render, redirect, get_object_or_404

from .forms import ResumeUploadForm
from .models import Resume, ResumeAnalysis

from .services.resume_parser import extract_resume_text
from .services.skill_extractor import extract_skills


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

                file_path = resume.resume_file.path

                # Extract text
                extracted_text = extract_resume_text(
                    file_path
                )

                resume.extracted_text = extracted_text
                resume.save()

                # Extract skills
                skills = extract_skills(
                    extracted_text
                )

                # Save analysis
                ResumeAnalysis.objects.update_or_create(
                    resume=resume,
                    defaults={
                        "extracted_skills": ", ".join(skills)
                    }
                )

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

    skills = []

    if analysis.extracted_skills:

        skills = [
            skill.strip()
            for skill in analysis.extracted_skills.split(",")
            if skill.strip()
        ]

    return render(
        request,
        "results.html",
        {
            "resume": resume,
            "skills": skills,
            "analysis": analysis
        }
    )