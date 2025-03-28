from fastapi import APIRouter, HTTPException
from app.services.transaction_service import transaction_service
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

class TransactionRequest(BaseModel):
    type: str
    fund_id: int
    amount: float

@router.get("/")
async def get_transactions():
    """Obtiene todas las transacciones"""
    return await transaction_service.get_all_transactions()

@router.post("/")
async def create_transaction(transaction: TransactionRequest):
    """Crea una nueva transacción"""
    try:
        return await transaction_service.add_transaction(transaction.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 