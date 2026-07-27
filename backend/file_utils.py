import fitz
from docx import Document


def extract_text(file_path):

    if file_path.lower().endswith(".pdf"):

        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()

        return text

    elif file_path.lower().endswith(".docx"):

        doc = Document(file_path)

        return "\n".join(
            p.text for p in doc.paragraphs
        )

    elif file_path.lower().endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    return ""