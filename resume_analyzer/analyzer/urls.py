from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_resume, name="upload_resume"),
    path(
        "success/<int:resume_id>/",
        views.upload_success,
        name="upload_success",
    ),
]