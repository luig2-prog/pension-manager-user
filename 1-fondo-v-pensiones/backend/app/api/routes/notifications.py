from fastapi import APIRouter, HTTPException

from app.api.models.notification import NotificationModel
from app.api.models.fund import FundModel
from app.api.schemas.notification import NotificationRequest, NotificationResponse

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
async def send_notification(notification_request: NotificationRequest):
    """Send a notification to the user about a fund subscription"""
    
    # Get fund information
    fund = await FundModel.get_fund(notification_request.fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    # Create notification message
    subject = f"Notificación - Fondo {fund['name']}"
    message = f"Usted se ha vinculado exitosamente al fondo {fund['name']} con un monto de COP {fund['min_amount']:,}."
    
    # Send notification
    result = await NotificationModel.send_notification(
        recipient=notification_request.recipient,
        message=message,
        subject=subject,
        notification_type=notification_request.notification_type
    )
    
    if not result.get("success", False):
        raise HTTPException(status_code=500, detail=result.get("message", "Error sending notification"))
    
    return result 