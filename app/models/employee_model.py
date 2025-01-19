from sqlalchemy import Column, Integer, String, ForeignKey,Enum as SQL_Enum
from app.database.base import base
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "employee"
    
class Employee(base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50), unique=True, index=True, nullable=False)
    emp_name = Column(String(100), index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(SQL_Enum(UserRole), default=UserRole.USER.value)
