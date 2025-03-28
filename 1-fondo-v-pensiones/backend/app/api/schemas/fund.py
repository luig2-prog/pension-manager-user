from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FundBase(BaseModel):
    id: str
    name: str
    min_amount: int
    category: str

class SubscribedFund(BaseModel):
    id: str
    name: str
    subscription_date: str
    amount: int

class UserFunds(BaseModel):
    user_id: str
    balance: int
    subscribed_funds: List[SubscribedFund]

class FundSubscriptionRequest(BaseModel):
    fund_id: str

class FundSubscriptionResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    new_balance: Optional[int] = None

class FundCancellationRequest(BaseModel):
    fund_id: str

class FundCancellationResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    new_balance: Optional[int] = None 