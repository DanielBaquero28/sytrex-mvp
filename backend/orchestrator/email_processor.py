import requests
import base64
from typing import Dict, Any
#import pydantic
import logging

logger = logging.getLogger(__name__)

# External service URLs
PARSE_EMAIL_URL = "http://localhost:8002/parse-email"
CLASSIFY_EMAIL_URL = "http://localhost:8004/classify"
TEXT_EXTRACT_URL = "http://localhost:8003/extract-text"
STORE_EMAIL_URL = "http://localhost:8001/store"

def process_email_pipeline(base64_email: str) -> Dict[str, Any]:
    """ Orchestrates the different microservices in a single function """

    # 1. Parse Email
    try:
        logger.info("Parsing email...")
        parse_response = requests.post(PARSE_EMAIL_URL, json={"file_type": "eml", "base64_file": base64_email})
        parse_response.raise_for_status()
        parsed_email = parse_response.json()
    except Exception as e:
        logger.error(f"Step 1: Email parsing failed - {e}")
        raise Exception(f"Step 1: Email parsing failed - {e}")
    

    # 2. Extract text from attachments
    try:
        attachments = parsed_email.get("attachments", [])
        extracted_texts = []

        for attachment in attachments:
            filename = attachment["filename"]
            file_type = filename.split(".")[-1].lower()

            if file_type in ["pdf", "docx"]:
                logger.info(f"Extracting text from attachment: {filename}")
                text_response = requests.post(TEXT_EXTRACT_URL, json={
                    "file_type": file_type,
                    "base64_file": attachment["base64_content"]
                })

                text_response.raise_for_status()
                extracted_texts.append(text_response.text)
            else:
                logger.info(f"Skipping unsupported attachment: {filename}")

    except Exception as e:
        logger.error(f"Step 2: Attachment extraction failed - {e}")
        raise Exception(f"Step 2: Attachment extraction failed - {e}")
    
    # 3. Classify email (Zero-shot)
    try:
        labels = ["Invoice", "Contract", "Job Application", "Spam", "Other"]
        combined_text = parsed_email["body"] + "\n" + "\n".join(extracted_texts)
        logger.info("Classifying combined email content...")
        classify_response = requests.post(CLASSIFY_EMAIL_URL, json={
            "content": combined_text,
            "labels": labels
        })

        classify_response.raise_for_status()
        classifications_results = classify_response.json()["classification"]
    except Exception as e:
        logger.error(f"Step 3: Classification failed - {e}")
        raise Exception(f"Step 3: Classification failed - {e}")
    
    # 4. Store email info with classifications
    try:
        storage_payload = {
            "sender": parsed_email["sender"],
            "subject": parsed_email["subject"],
            "received_at": parsed_email["received_at"],
            "body": parsed_email["body"],
            "classifications": [
                {"label": c["label"], "score": c["score"]}
                for c in classifications_results
            ],
            "attachments": [
                {
                    "filename": a["filename"],
                    "content_type": a["content_type"]
                } for a in attachments
            ]
        }

        print(f"Storage Payload: {storage_payload}")

        logger.info("Storing parsed email into DB...")
        store_response = requests.post(STORE_EMAIL_URL, json=storage_payload)
        store_response.raise_for_status()

        logger.info("Email successfully stored.")
        return store_response.json()
    except Exception as e:
        logger.error(f"Step 4: Email storage failed - {e}")
        raise Exception(f"Step 4: Email storage failed - {e}")