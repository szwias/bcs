from PyPDF2 import PdfReader


def extract_text_from_pdf(file_obj):
    """Extract text from a PDF file object."""
    file_obj.open("rb")  # Ensure file is open in binary mode
    reader = PdfReader(file_obj)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)
