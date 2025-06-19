from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.classifier import ZeroShotEmailClassifier
from typing import List

from app.db.database import Base, engine
from app.db import models
from app.api.routes.classifier_api import router as classifier_router

Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()
# Create instance of Facebook Bart Large MNLI model
classifier = ZeroShotEmailClassifier()

app.include_router(classifier_router)

class ClassifierRequest(BaseModel):
    content: str
    labels: List[str]

@app.post("/classify")
def classify_email(request: ClassifierRequest):
    """ Classifies email using email content and Hugging Face AI model """
    try:
        result = classifier.classify(request.content, request.labels)
        rounded_scores = [round(score, 3) for score in result["scores"]]
        sorted_results = sorted(
            zip(result["labels"], rounded_scores),
            key=lambda x: x[1],
            reverse=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error ocurred {str(e)}")
    
    return {"classification": [{"label": lbl, "score": scr} for lbl, scr in sorted_results]}