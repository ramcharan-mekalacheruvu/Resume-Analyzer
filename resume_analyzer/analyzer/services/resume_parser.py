import os

from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .text_cleaner import clean_text


def extract_resume_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        text = extract_text_from_pdf(file_path)

    elif extension == ".docx":

        text = extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Only PDF and DOCX files are supported."
        )

    return clean_text(text)