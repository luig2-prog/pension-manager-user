from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FundBase(BaseModel):
    nombre: str
    monto_minimo: float
    categoria: str

class Fund(FundBase):
    id: int

    class Config:
        from_attributes = True

class SubscribedFund(BaseModel):
    id: str
    name: str
    subscription_date: str
    amount: float

class UserFunds(BaseModel):
    balance: float
    subscribed_funds: List[SubscribedFund]

class FundSubscriptionRequest(BaseModel):
    fund_id: int

class FundSubscriptionResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    new_balance: Optional[float] = None

class FundCancellationRequest(BaseModel):
    fund_id: str

class FundCancellationResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    new_balance: Optional[float] = None 