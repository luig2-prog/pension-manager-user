from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models.transaction import TransactionModel
from app.api.schemas.transaction import TransactionResponse

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(user_id: str = "default_user"):
    """
    Obtener el historial de transacciones del usuario
    """
    return await TransactionModel.get_user_transactions(user_id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    transaction = await TransactionModel.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction 