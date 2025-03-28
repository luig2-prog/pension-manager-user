from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models.fund import FundModel
from app.api.schemas.fund import (
    Fund,
    UserFunds,
    FundSubscriptionRequest,
    FundSubscriptionResponse,
    FundCancellationRequest,
    FundCancellationResponse
)

router = APIRouter()

@router.get("/", response_model=List[Fund])
async def read_funds():
    """
    Obtener todos los fondos disponibles
    """
    return await FundModel.get_all_funds()

@router.get("/user", response_model=UserFunds)
async def get_user_funds(user_id: str = "default_user"):
    """Get user's balance and subscribed funds"""
    return await FundModel.get_user_funds(user_id)

@router.get("/{fund_id}", response_model=Fund)
async def read_fund(fund_id: int):
    """
    Obtener un fondo específico por su ID
    """
    fund = await FundModel.get_fund(fund_id)
    if fund is None:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")
    return fund

@router.post("/subscribe", response_model=FundSubscriptionResponse)
async def subscribe_to_fund(
    subscription: FundSubscriptionRequest, 
    user_id: str = "default_user"
):
    """Subscribe to a fund"""
    try:
        return await FundModel.subscribe_to_fund(
            user_id=user_id,
            fund_id=subscription.fund_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/unsubscribe", response_model=FundCancellationResponse)
async def unsubscribe_from_fund(
    cancellation: FundCancellationRequest, 
    user_id: str = "default_user"
):
    """Unsubscribe from a fund"""
    try:
        return await FundModel.unsubscribe_from_fund(
            user_id=user_id,
            fund_id=cancellation.fund_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 