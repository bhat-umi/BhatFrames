from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Enum as SQLALchemyEnum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database.base import base
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    
class PaymentMethod(Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    CHEQUE = "cheque"


class Payment(base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), index=True)
    employee_id = Column(String, ForeignKey('employee.emp_id'), index=True)
    payment_amount = Column(Integer)
    payment_method = Column(SQLALchemyEnum(PaymentMethod), index=True)
    payment_uid = Column(String, index=True, unique=True)
    comments = Column(String)
    payment_date = Column(Date, index=True)  # Changed to Date type
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    customer = relationship("Customer", back_populates="payments")
    employee = relationship("Employee", back_populates="payments")
