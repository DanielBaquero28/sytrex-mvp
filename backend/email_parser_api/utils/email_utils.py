import base64
from email import message_from_bytes
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import List, Tuple, Optional
from datetime import datetime
#from io import BytesIO

def parse_email_from_base64(base64_email: str) -> Tuple[str, str, datetime, str, List[Tuple[str, str, str]]]:
    """ Parses a base64-encoded email file (.eml) and extracts relevant fields.
    sender: str, subject: str, received_at: datetime, body: str, attachments List of tuples, inside filename: str, content_type: str, base64_content: str
    """
    # Decodes email
    email_bytes = base64.b64decode(base64_email)

    #
    msg: Message = message_from_bytes(email_bytes)

    sender = msg.get("From", "")
    subject = msg.get("Subject", "")
    received_at = None

    try:
        if msg.get("Date"):
            received_at = parsedate_to_datetime(msg.get("Date"))
    except Exception as e:
        received_at = datetime.now()

    if received_at is None:
        received_at = datetime.now()

    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", "")
            content_type = part.get_content_type()

            if content_disposition and "attachment" in content_disposition:
                filename = part.get_filename()
                file_data = part.get_payload(decode=True)
                base64_content = base64.b64encode(file_data).decode("utf-8")
                attachments.append((filename, content_type, base64_content))
            elif content_type == "text/plain" and not body:
                body = part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return sender, subject, received_at, body, attachments