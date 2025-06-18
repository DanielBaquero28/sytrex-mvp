from fastapi import FastAPI, HTTPException
from schemas import ParsedEmail, ParsedAttachment, EmailParseRequest
from utils.email_utils import parse_email_from_base64

# Initialize FastAPI app
app = FastAPI()

@app.post("/parse-email", response_model=ParsedEmail)
def parse_email(file_request: EmailParseRequest):
    """ Parses base64 email """
    try:
        if file_request.file_type != "eml":
            raise HTTPException(status_code=400, detail="Only .eml files are supported")
        
        sender, subject, received_at, body, attachments = parse_email_from_base64(file_request.base64_file)

        parsed_attachments = [
            ParsedAttachment(
                filename=filename,
                content_type=content_type,
                base64_content=base64_content
            ) for filename, content_type, base64_content in attachments
        ]

        #result = parse_email_from_base64(file_request.base64_eml)
        return ParsedEmail(
            sender=sender,
            subject=subject,
            received_at=received_at,
            body=body,
            attachments=parsed_attachments
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email parsing failed: {str(e)}")