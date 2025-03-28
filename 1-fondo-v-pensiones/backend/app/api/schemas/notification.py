from pydantic import BaseModel, EmailStr
from typing import Optional

class NotificationRequest(BaseModel):
    recipient: str  # Email or phone number
    fund_id: str
    notification_type: str = "email"  # "email" or "sms"

class NotificationResponse(BaseModel):
    success: bool
    message: str
    message_id: Optional[str] = None 