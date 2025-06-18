from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from .database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    subject = Column(String)
    received_at = Column(DateTime)
    body = Column(String)
    classifications = relationship("Classification", back_populates="email", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="email", cascade="all, delete-orphan")

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    score = Column(Float)
    email_id = Column(Integer, ForeignKey("emails.id"))
    email = relationship("Email", back_populates="classifications")

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content_type = Column(String)
    email_id = Column(Integer, ForeignKey("emails.id"))
    email = relationship("Email", back_populates="attachments")
