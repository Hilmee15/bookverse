"""BookVerse API - FastAPI application.

Endpoints
---------
GET  /health       -> liveness probe (checks PostgreSQL + Redis connectivity)
GET  /api/books    -> READ  : list catalog (supports ?search= and ?genre=)
POST /api/predict  -> WRITE : AI recommendation (TF-IDF + cosine similarity),
                             result cached in Redis, history saved to PostgreSQL
GET  /api/history  -> READ  : recent recommendation history from PostgreSQL
"""
from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager

import redis as redis_lib
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .cover_urls import COVER_URLS
from .database import Base, SessionLocal, engine, get_db
from .models import Book, RecommendationHistory
from .recommender import recommender
from .seed_data import BOOKS

CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))


# ----------------------------------------------------------------- startup
def _seed_and_fit() -> None:
    """Create tables, seed catalog once (idempotent), fit the TF-IDF model."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        count = db.scalar(select(func.count(Book.id)))
        if count == 0:
            db.add_all(
                Book(**b, cover_url=COVER_URLS.get(b["title"])) for b in BOOKS
            )
            db.commit()
        books = [
            {
                "id": b.id, "title": b.title, "author": b.author,
                "genre": b.genre, "year": b.year, "rating": b.rating,
                "description": b.description, "cover_url": b.cover_url,
            }
            for b in db.scalars(select(Book)).all()
        ]
    recommender.fit(books)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _seed_and_fit()
    yield


app = FastAPI(
    title="BookVerse API",
    description="AI book & novel recommender - UTS COMP6991031",
    version="1.0.0",
    lifespan=lifespan,
)

# The nginx frontend proxies /api to this backend (same origin), so CORS is
# not needed in production; this is only a convenience for local dev servers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_redis = redis_lib.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))


# ----------------------------------------------------------------- schemas
class PredictRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=300,
                       description="A book title you like (mode=title) or free text (mode=text)")
    mode: str = Field("title", pattern="^(title|text)$")
    top_n: int = Field(6, ge=1, le=12)


# ----------------------------------------------------------------- helpers
def _cache_key(req: PredictRequest) -> str:
    return f"rec:{req.mode}:{req.query.strip().lower()}:{req.top_n}"


# ----------------------------------------------------------------- routes
@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Liveness probe: verify PostgreSQL and Redis are reachable."""
    checks = {}
    try:
        db.execute(select(1))
        checks["database"] = "connected"
    except Exception:
        checks["database"] = "unreachable"
    try:
        checks["redis"] = "connected" if _redis.ping() else "unreachable"
    except Exception:
        checks["redis"] = "unreachable"

    status = "ok" if all(v == "connected" for v in checks.values()) else "degraded"
    code = 200 if status == "ok" else 503
    return {"status": status, "code": code, "checks": checks}


@app.get("/api/books")
def list_books(search: str = "", genre: str = "", db: Session = Depends(get_db)):
    """READ endpoint: catalog with optional search + genre filter."""
    stmt = select(Book)
    if search:
        like = f"%{search.strip()}%"
        stmt = stmt.where((Book.title.ilike(like)) | (Book.author.ilike(like)))
    if genre:
        stmt = stmt.where(Book.genre == genre)
    books = db.scalars(stmt).all()
    genres = sorted({b.genre for b in db.scalars(select(Book)).all()})
    return {
        "total": len(books),
        "genres": genres,
        "books": [
            {"id": b.id, "title": b.title, "author": b.author, "genre": b.genre,
             "year": b.year, "rating": b.rating, "description": b.description,
             "cover_url": b.cover_url}
            for b in books
        ],
    }


@app.post("/api/predict", status_code=201)
def predict(req: PredictRequest):
    """WRITE endpoint: compute recommendations, cache in Redis, log to PostgreSQL."""
    key = _cache_key(req)
    cached = None
    try:
        raw = _redis.get(key)
        cached = json.loads(raw) if raw else None
    except Exception:
        cached = None  # Redis is optional: fall back to computing

    if cached is not None:
        result = cached
        result["cached"] = True
    else:
        if req.mode == "title":
            result = recommender.recommend_from_title(req.query, req.top_n)
            if result is None:  # unknown title -> helpful 404
                raise HTTPException(
                    status_code=404,
                    detail=f"Book '{req.query}' not found. Try GET /api/books for the catalog.",
                )
        else:
            result = recommender.recommend_from_text(req.query, req.top_n)
        result["cached"] = False
        try:
            _redis.setex(key, CACHE_TTL, json.dumps(result))
        except Exception:
            pass  # cache is best-effort

    # Persist every prediction as history (the DB write requirement)
    history = RecommendationHistory(
        query=req.query.strip(),
        mode=req.mode,
        results=result["recommendations"],
    )
    with SessionLocal() as db:
        db.add(history)
        db.commit()

    return result


@app.get("/api/history")
def history(limit: int = 10):
    """READ endpoint: the most recent recommendations stored in PostgreSQL."""
    with SessionLocal() as db:
        rows = db.scalars(
            select(RecommendationHistory).order_by(RecommendationHistory.id.desc()).limit(min(limit, 50))
        ).all()
    return {
        "total": len(rows),
        "items": [
            {"id": r.id, "query": r.query, "mode": r.mode,
             "results": r.results, "created_at": r.created_at.isoformat()}
            for r in rows
        ],
    }
