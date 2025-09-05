from textwrap import shorten
import PyPDF2
from core.utils.Lengths import SNIPPET_LENGTH


def snip(instance, text):
    title = instance._meta.verbose_name
    desc = shorten(text, width=SNIPPET_LENGTH, placeholder="...")
    return f"{title}: [{desc}]"


def extract_text_from_pdf(file_obj):
    """Extract text from a PDF file object."""
    file_obj.open('rb')  # Ensure file is open in binary mode
    reader = PyPDF2.PdfReader(file_obj)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


