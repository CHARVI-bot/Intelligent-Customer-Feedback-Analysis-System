from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
import analyzer

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./feedback.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FeedbackDB(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    feedback_text = Column(Text)
    rating = Column(Integer)
    sentiment = Column(String)
    sentiment_score = Column(Float)
    themes = Column(String) # Comma separated
    urgency = Column(String)
    created_at = Column(String)

Base.metadata.create_all(bind=engine)

# Schemas
class FeedbackCreate(BaseModel):
    customer_name: str
    feedback_text: str
    rating: int

class FeedbackResponse(FeedbackCreate):
    id: int
    sentiment: str
    sentiment_score: float
    themes: str
    urgency: str
    created_at: str

    class Config:
        from_attributes = True

# App setup
app = FastAPI(title="Intelligent Customer Feedback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/feedback", response_model=FeedbackResponse)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    # Analyze feedback intelligently
    analysis = analyzer.analyze_text(feedback.feedback_text, feedback.rating)
    
    db_feedback = FeedbackDB(
        customer_name=feedback.customer_name,
        feedback_text=feedback.feedback_text,
        rating=feedback.rating,
        sentiment=analysis["sentiment"],
        sentiment_score=analysis["sentiment_score"],
        themes=",".join(analysis["themes"]),
        urgency=analysis["urgency"],
        created_at=datetime.now().isoformat()
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/api/feedbacks", response_model=List[FeedbackResponse])
def get_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = db.query(FeedbackDB).order_by(FeedbackDB.id.desc()).offset(skip).limit(limit).all()
    return feedbacks

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    feedbacks = db.query(FeedbackDB).all()
    total = len(feedbacks)
    if total == 0:
        return {"total": 0, "positive": 0, "neutral": 0, "negative": 0, "average_rating": 0}
    
    positive = sum(1 for f in feedbacks if f.sentiment == "Positive")
    neutral = sum(1 for f in feedbacks if f.sentiment == "Neutral")
    negative = sum(1 for f in feedbacks if f.sentiment == "Negative")
    avg_rating = sum(f.rating for f in feedbacks) / total

    return {
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "average_rating": round(avg_rating, 2)
    }

# Ensure frontend directory exists
os.makedirs("frontend", exist_ok=True)
# Serve static files (Frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
