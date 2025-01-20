from pydantic import BaseModel
from enum import Enum


class Title(Enum):
    MR = "Mr"
    MS = "Ms"
    

class Create_Customer(BaseModel):
    title: Title
    customer_first_name: str
    customer_last_name: str
    customer_address: str
    customer_contact: str