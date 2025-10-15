from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from . import models
from .schemas import ReviewCreate, ReviewRead
from .llm import review_code


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Code Review Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/review", response_model=ReviewRead)
async def create_review(
    file: UploadFile | None = File(default=None),
    content: str | None = Form(default=None),
    filename: str | None = Form(default=None),
    language: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    if not file and not content:
        raise HTTPException(status_code=400, detail="Provide either a file or content.")

    if file:
        raw = await file.read()
        content_text = raw.decode("utf-8", errors="replace")
        filename_val = file.filename or filename or "uploaded.txt"
    else:
        content_text = content or ""
        filename_val = filename or "snippet.txt"

    if not content_text.strip():
        raise HTTPException(status_code=400, detail="Content is empty.")

    report = review_code(filename_val, language, content_text)

    review = models.Review(
        filename=filename_val,
        language=language,
        content=content_text,
        report=report,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@app.get("/api/reviews", response_model=list[ReviewRead])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(models.Review).order_by(models.Review.created_at.desc()).limit(100).all()


@app.get("/api/reviews/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


