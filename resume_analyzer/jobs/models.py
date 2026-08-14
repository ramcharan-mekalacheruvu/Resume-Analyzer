from django.db import models


class Job(models.Model):

    title = models.CharField(max_length=200)

    company = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField()

    required_skills = models.TextField()

    location = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.title