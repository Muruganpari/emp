from typing import Text
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base

class Employee(Base):
    __tablename__ = "Employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    email = Column(Text())
    age = Column(String(20))
    designation = Column(String(100))
