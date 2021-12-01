from datetime import date
from pydantic import BaseModel


class Employee(BaseModel):
    id = int
    name = str
    email = str
    designation = str
    age = str
    data = date

    class Config:
        orm_mode = True