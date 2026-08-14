from django.db import models


class Resume(models.Model):

    resume_file = models.FileField(
        upload_to="resumes/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.resume_file.name


class ResumeAnalysis(models.Model):

    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE
    )

    ats_score = models.IntegerField(
        default=0
    )

    extracted_skills = models.TextField(
        blank=True
    )

    recommended_jobs = models.TextField(
        blank=True
    )

    missing_skills = models.TextField(
        blank=True
    )

    analyzed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Analysis for "
            f"{self.resume.resume_file.name}"
        )