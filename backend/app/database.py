"""Database engine and session setup (SQLAlchemy + PostgreSQL)."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL comes from the .env file, e.g.
# postgresql+psycopg2://bookuser:bookpass@db:5432/bookverse
# The host "db" is the docker compose SERVICE NAME, resolved
# through the user-defined network - not localhost.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://bookuser:bookpass@db:5432/bookverse")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: open a session, guarantee it is closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
