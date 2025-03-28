from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: str
    user_id: str
    fund_id: int
    fund_name: str
    type: str  # "SUBSCRIPTION" or "CANCELLATION"
    amount: float
    timestamp: str

class TransactionResponse(BaseModel):
    id: str
    fund_name: str
    type: str
    amount: float
    timestamp: str 