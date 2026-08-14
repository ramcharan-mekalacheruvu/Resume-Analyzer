import pdfplumber


def extract_text_from_pdf(file_path):
    """
    Extract text from all pages of a PDF resume.
    """

    extracted_text = []

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    extracted_text.append(text)

    except Exception as e:
        raise ValueError(
            f"Unable to read PDF file: {str(e)}"
        )

    return "\n".join(extracted_text)