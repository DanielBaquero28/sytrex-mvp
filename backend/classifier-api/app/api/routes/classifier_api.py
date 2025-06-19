from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import EmailCreate
from app.db.models import Attachment, Email, Classification
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/store")
def store_classification(email_payload: EmailCreate, db: Session = Depends(get_db)):
    """ Endpoint for storing email classification into our database """
    # Save email
    email = Email(
        sender = email_payload.sender,
        subject = email_payload.subject,
        received_at = email_payload.received_at,
        body = email_payload.body
    )

    # Checking for email duplicates
    existing_email = db.query(Email).filter_by(
    sender=email.sender,
    subject=email.subject,
    received_at=email.received_at
    ).first()

    if existing_email:
        return JSONResponse(
            content={"message": "Email already exists."},
            status_code=409
        )

    try:
        db.add(email)
        db.commit()
        db.refresh(email)

        # Save classification
        for cls in email_payload.classifications:
            classification = Classification(
                label = cls.label,
                score = round(cls.score, 4),
                email_id = email.id
            )
            db.add(classification)

        # Save attachments if any since it's optional
        if email_payload.attachments:
            for att in email_payload.attachments:
                attachment = Attachment(
                    filename=att.filename,
                    content_type=att.content_type,
                    email_id=email.id
                )
                db.add(attachment)

        db.commit()

        return JSONResponse(
            content={"message": "Email and related data stored successfully."},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {e}")