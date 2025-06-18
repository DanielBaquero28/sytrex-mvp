from docx import Document
import base64
from io import BytesIO

def extract_text_from_docx(base64_docx: str) -> str:
    """ Reads from base64 encoded DOCX and returns str text """
    docx_bytes = base64.b64decode(base64_docx)
    docx_stream = BytesIO(docx_bytes)
    doc = Document(docx_stream)

    full_text = []
    for p in doc.paragraphs:
        full_text.append(p.text)
    
    return '\n'.join(full_text)
