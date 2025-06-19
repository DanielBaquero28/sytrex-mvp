from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api.routes.classifier_api import router as classifier_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(classifier_router)