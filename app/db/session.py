# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# connect_args for sqlite in multithread dev env
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()

# Dependency for FastAPI (if you use Depends(get_db) in endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()