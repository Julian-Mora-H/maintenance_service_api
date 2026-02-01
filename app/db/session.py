# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# connect_args para sqlite en multithread dev env
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()

# Dependency para FastAPI (si usas Depends(get_db) en endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()