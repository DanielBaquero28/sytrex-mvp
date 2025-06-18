from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.pdf_utils import extract_text_from_pdf
from utils.docx_utils import extract_text_from_docx
#from utils.email_utils import parse_email_from_base64
#from schemas import ParsedEmail, ParsedAttachment

# Initialize FastAPI app
app = FastAPI()

class FileExtractRequest(BaseModel):
    file_type: str
    base64_file: str

@app.post("/extract-text")
def extract_text(file_request: FileExtractRequest):
    """ Extracts data from PDF and DOCX files """
    try:
        if file_request.file_type == "pdf":
            text = extract_text_from_pdf(file_request.base64_file)
        elif file_request.file_type == "docx":
            text = extract_text_from_docx(file_request.base64_file)
        else:
            raise HTTPException(status_code=400, detail="File type is not supported")
    
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")
