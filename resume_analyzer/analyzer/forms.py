from django import forms

from .models import Resume


class ResumeUploadForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ["resume_file"]

        widgets = {
            "resume_file": forms.ClearableFileInput(
                attrs={
                    "accept": ".pdf,.docx"
                }
            )
        }

    def clean_resume_file(self):

        file = self.cleaned_data["resume_file"]

        allowed_extensions = [".pdf", ".docx"]

        file_extension = "." + file.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        # 5 MB limit
        max_size = 5 * 1024 * 1024

        if file.size > max_size:
            raise forms.ValidationError(
                "File size must be less than 5 MB."
            )

        return file