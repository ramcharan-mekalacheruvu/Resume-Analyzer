from django.contrib import admin
from .models import Resume, ResumeAnalysis


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "resume_file",
        "uploaded_at",
    )


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "resume",
        "ats_score",
        "analyzed_at",
    )