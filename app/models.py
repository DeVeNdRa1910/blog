from sqlalchemy import Column, Integer, String
from .db import Base

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)
    body = Column(String)