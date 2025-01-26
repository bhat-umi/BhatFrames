from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLALchemyEnum
from app.database.base import base
from enum import Enum
from sqlalchemy.orm import relationship

class Title(Enum):
    Mr = "Mr"    # Match exact database enum values
    Ms = "Ms"    # Match exact database enum values

class Customer(base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    title = Column(SQLALchemyEnum(Title), index=True)
    customer_first_name = Column(String)
    customer_last_name = Column(String)
    customer_address = Column(String)
    customer_contact = Column(String, index=True, unique=True)
    balance = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    payments = relationship("Payment", back_populates="customer")
    
    