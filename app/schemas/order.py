from pydantic import BaseModel,ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    item_id: int
    quantity: int = 1

class OrderCreate(BaseModel):
    report: str
    items: List[OrderItem]
    request_id: Optional[str] = None # Para la clave de idempotencia

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    report: str
    items: List[OrderItem]
    created_at: Optional[datetime] = None
