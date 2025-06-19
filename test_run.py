import base64
from backend.orchestrator.email_processor import process_email_pipeline

# Load and encode sample email
with open("sample_email.eml", "rb") as f:
    base64_email = base64.b64encode(f.read()).decode("utf-8")

# Call the orchestrator
try:
    result = process_email_pipeline(base64_email)
    print("✅ Pipeline result:")
    print(result)
except Exception as e:
    print("❌ Pipeline failed:")
    print(e)