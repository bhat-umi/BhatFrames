from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class PaymentMethod(Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    CHEQUE = "cheque"

class PaymentCreate(BaseModel):
    customer_id: int
    amount: float
    payment_date: date = Field(default_factory=date.today)
    payment_method: PaymentMethod
    payment_uid: str
    comments: str