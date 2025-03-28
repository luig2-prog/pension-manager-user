from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    id: str
    user_id: str
    fund_id: str
    fund_name: str
    type: str  # "SUBSCRIPTION" or "CANCELLATION"
    amount: int
    timestamp: str 