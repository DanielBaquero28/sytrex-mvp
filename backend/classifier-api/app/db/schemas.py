from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClassificationBase(BaseModel):
    label: str
    score: float

class AttachmentBase(BaseModel):
    filename: str
    content_type: str

class EmailBase(BaseModel):
    sender: str
    subject: str
    received_at: datetime
    body: Optional[str]
    classifications: List[ClassificationBase]
    attachments: List[AttachmentBase]

class EmailCreate(BaseModel):
    sender: str
    subject: str
    received_at: datetime
    body: Optional[str]
    classifications: List[ClassificationBase]
    attachments: Optional[List[AttachmentBase]] = []

class EmailInDB(EmailBase):
    id: int

    class Config:
        orm_mode = True