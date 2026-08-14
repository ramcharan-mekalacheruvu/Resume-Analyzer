from django.shortcuts import render, redirect

from .forms import ResumeUploadForm


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

            return redirect(
                "upload_success",
                resume_id=resume.id
            )

    else:

        form = ResumeUploadForm()

    return render(
        request,
        "upload.html",
        {"form": form}
    )


def upload_success(request, resume_id):

    return render(
        request,
        "results.html",
        {
            "resume_id": resume_id
        }
    )