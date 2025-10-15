from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from .db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    language = Column(String(64), nullable=True)
    content = Column(Text, nullable=False)
    report = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


