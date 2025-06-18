import fitz
import base64
from io import BytesIO

def extract_text_from_pdf(base64_pdf: str) -> str:
    """ Reads from base64 encoded PDF and returns str text """
    pdf_bytes = base64.b64decode(base64_pdf)
    pdf_stream = BytesIO(pdf_bytes)
    text = ""

    with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
        
    return text