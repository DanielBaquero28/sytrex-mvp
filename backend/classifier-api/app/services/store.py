from sqlalchemy.orm import Session
from ..db import models
from ..db.database import SessionLocal

def store_email_classification(email_data):
    db: Session = SessionLocal()
    try:
        email = models.Email(
            sender=email_data["sender"],
            subject=email_data["subject"],
            received_at=email_data["received_at"],
            body=email_data.get("body", "")
        )
        db.add(email)
        db.flush()  # Assign email.id

        for cls in email_data["classifications"]:
            db.add(models.Classification(label=cls["label"], score=cls["score"], email_id=email.id))

        for att in email_data["attachments"]:
            db.add(models.Attachment(filename=att["filename"], content_type=att["content_type"], email_id=email.id))

        db.commit()
        return {"status": "success", "email_id": email.id}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()