from enum import Enum
from pydantic import BaseModel, EmailStr, constr

class NotificationType(str, Enum):
    email = "email"
    sms = "sms"

class NotificationRequest(BaseModel):
    fund_id: int
    notification_type: NotificationType
    contact_info: str  # Email o número de teléfono

class NotificationResponse(BaseModel):
    message: str
    id: str 