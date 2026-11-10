"""SQLAlchemy ORM models: books catalog + recommendation history."""
from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text, func

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    genre = Column(String(64), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False, default=0.0)
    description = Column(Text, nullable=False)
    # Public cover image URL (Google Books / Open Library CDN);
    # NULL -> frontend falls back to the generated CSS cover.
    cover_url = Column(String(512), nullable=True)


class RecommendationHistory(Base):
    """One row per POST /api/predict call - proves the WRITE path to PostgreSQL."""

    __tablename__ = "recommendation_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    mode = Column(String(16), nullable=False)  # "title" | "text"
    results = Column(JSON, nullable=False)  # [{id, title, author, genre, similarity}]
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
