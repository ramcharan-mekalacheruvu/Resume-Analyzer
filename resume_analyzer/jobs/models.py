from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    skills = models.TextField(
        help_text="Separate skills using commas or |"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title