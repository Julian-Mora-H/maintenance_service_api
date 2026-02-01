from sqlalchemy import Column, Integer, String , DateTime, func
from app.db.session import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    id = Column(Integer, primary_key=True, index=True)
    request_key = Column(String, unique=True, nullable=False, index=True)
    resource_type = Column(String, nullable=False)
    resource_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)