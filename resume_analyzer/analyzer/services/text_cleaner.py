import re


def clean_text(text):
    """
    Clean extracted resume text.
    """

    if not text:
        return ""

    # Replace multiple spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n+", "\n", text)

    # Remove unwanted characters
    text = re.sub(
        r"[^\w\s.,;:/@+#&()%-]",
        "",
        text
    )

    return text.strip()