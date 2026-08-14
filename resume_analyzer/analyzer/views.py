from django.shortcuts import render, redirect

from .forms import ResumeUploadForm
from .services.resume_parser import extract_resume_text


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

                extracted_text = extract_resume_text(
                    file_path
                )

                resume.extracted_text = extracted_text
                resume.save()

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
        {"form": form}
    )


def upload_success(request, resume_id):

    from .models import Resume

    resume = Resume.objects.get(
        id=resume_id
    )

    return render(
        request,
        "results.html",
        {
            "resume": resume
        }
    )