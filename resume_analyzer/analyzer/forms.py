from django import forms
from .models import Resume


class ResumeUploadForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ["resume_file"]

    def clean_resume_file(self):

        file = self.cleaned_data["resume_file"]

        allowed_extensions = [".pdf", ".docx"]

        filename = file.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        max_size = 5 * 1024 * 1024

        if file.size > max_size:
            raise forms.ValidationError(
                "Resume size must be less than 5 MB."
            )

        return file