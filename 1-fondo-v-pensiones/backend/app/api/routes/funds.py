from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.api.models.fund import FundModel
from app.api.schemas.fund import (
    FundBase, 
    UserFunds, 
    FundSubscriptionRequest, 
    FundSubscriptionResponse,
    FundCancellationRequest,
    FundCancellationResponse
)

router = APIRouter()

@router.get("/", response_model=List[FundBase])
async def get_all_funds():
    """Get all available funds"""
    funds = await FundModel.get_all_funds()
    return funds

@router.get("/user", response_model=UserFunds)
async def get_user_funds(user_id: str = "default_user"):
    """Get user's balance and subscribed funds"""
    user_data = await FundModel.get_user_data(user_id)
    return user_data

@router.post("/subscribe", response_model=FundSubscriptionResponse)
async def subscribe_to_fund(
    subscription: FundSubscriptionRequest, 
    user_id: str = "default_user"
):
    """Subscribe to a fund"""
    result = await FundModel.subscribe_to_fund(user_id, subscription.fund_id)
    if not result.get("success", False):
        # Return 400 for client errors, but keep the detailed message
        raise HTTPException(status_code=400, detail=result.get("message", "Error subscribing to fund"))
    return result

@router.post("/unsubscribe", response_model=FundCancellationResponse)
async def unsubscribe_from_fund(
    cancellation: FundCancellationRequest, 
    user_id: str = "default_user"
):
    """Unsubscribe from a fund"""
    result = await FundModel.unsubscribe_from_fund(user_id, cancellation.fund_id)
    if not result.get("success", False):
        # Return 400 for client errors, but keep the detailed message
        raise HTTPException(status_code=400, detail=result.get("message", "Error unsubscribing from fund"))
    return result 