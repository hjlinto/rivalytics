from sqlalchemy import Column, Integer, String
from database import Base

# Hero class definition
class Hero(Base):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)