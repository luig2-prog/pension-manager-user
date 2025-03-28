from fastapi import APIRouter, HTTPException
from app.services.fund_service import fund_service
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/funds",
    tags=["funds"]
)

class SubscriptionRequest(BaseModel):
    fund_id: int

@router.get("/")
async def get_funds():
    """Obtiene todos los fondos disponibles"""
    return await fund_service.get_all_funds()

@router.get("/user")
async def get_user_subscriptions():
    """Obtiene las suscripciones del usuario actual"""
    return await fund_service.get_user_subscriptions()

@router.get("/{fund_id}")
async def get_fund(fund_id: int):
    """Obtiene un fondo específico por su ID"""
    return await fund_service.get_fund(fund_id)

@router.post("/subscribe")
async def subscribe_to_fund(subscription: SubscriptionRequest):
    """Suscribe un usuario a un fondo"""
    try:
        return await fund_service.subscribe(subscription.fund_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 