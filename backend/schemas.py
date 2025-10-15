from datetime import datetime
from pydantic import BaseModel


class ReviewCreate(BaseModel):
    filename: str
    language: str | None = None
    content: str


class ReviewRead(BaseModel):
    id: int
    filename: str
    language: str | None
    content: str
    report: str
    created_at: datetime

    class Config:
        from_attributes = True


