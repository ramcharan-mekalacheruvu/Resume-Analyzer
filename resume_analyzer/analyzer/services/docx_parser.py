from docx import Document


def extract_text_from_docx(file_path):
    """
    Extract text from paragraphs in a DOCX resume.
    """

    extracted_text = []

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                extracted_text.append(text)

    except Exception as e:
        raise ValueError(
            f"Unable to read DOCX file: {str(e)}"
        )

    return "\n".join(extracted_text)