from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models.transaction import TransactionModel
from app.api.schemas.transaction import Transaction

router = APIRouter()

@router.get("/", response_model=List[Transaction])
async def get_transactions(user_id: str = "default_user"):
    """Get all transactions for a user"""
    transactions = await TransactionModel.get_transactions(user_id)
    return transactions

@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    transaction = await TransactionModel.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction 