from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ParsedAttachment(BaseModel):
    filename: str
    content_type: str

class ParsedClassification(BaseModel):
    label: str
    score: float

class ParsedEmail(BaseModel):
    sender: str
    subject: str
    received_at: datetime
    body: Optional[str]
    attachments: Optional[List[ParsedAttachment]] = []
    classifications: List[ParsedClassification] = []

class EmailParseRequest(BaseModel):
    file_type: str
    base64_file: str