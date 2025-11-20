from fastapi import APIRouter, Depends, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from .conversation import handle_inbound_message

router = APIRouter()

@router.post("/webhook/twilio")
async def twilio_webhook(From: str = Form(...), Body: str = Form(...), db: AsyncSession = Depends(get_db)):
    """
    Twilio will POST form fields including:
      - From: "whatsapp:+1415XXXXXXX"
      - Body: message text
    """
    # normalize contact number (remove 'whatsapp:' prefix if present)
    contact = From.replace("whatsapp:", "").strip()
    text = Body or ""

    reply_text, finished = await handle_inbound_message(db, contact, text)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return Response(content=str(twiml), media_type="text/xml")
