from fastapi import APIRouter, HTTPException
from app.models.notification import NotificationRequest, NotificationResponse, NotificationType
from app.services.fund_service import fund_service
from app.services.notification_service import notification_service

router = APIRouter(
    prefix="/api/notifications",
    tags=["notifications"]
)

@router.post("/send", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest):
    # Verificar que el fondo existe
    fund = await fund_service.get_fund(request.fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    success = False
    if request.notification_type == NotificationType.email:
        success = await notification_service.send_email(request.contact_info, fund)
    elif request.notification_type == NotificationType.sms:
        success = await notification_service.send_sms(request.contact_info, fund)

    if not success:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar la notificación por {request.notification_type}"
        )

    return NotificationResponse(
        message=f"Notificación enviada exitosamente por {request.notification_type}",
        id=str(request.fund_id)
    ) 