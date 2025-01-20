from pydantic import BaseModel
from enum import Enum


class Title(Enum):
    MR = "Mr"
    MS = "Ms"
    

class Create_Customer(BaseModel):
    title: Title
    fname: str
    lname: str
    address: str
    contact: str
    balance:int