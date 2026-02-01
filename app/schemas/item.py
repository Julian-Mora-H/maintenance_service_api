from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ItemBase(BaseModel):
    name: str = Field(..., example="Filtro de Aire")
    sku: str = Field(..., example="SKU-3126")
    price: float = Field(..., example=49.99)
    stock: int = Field(..., example=100)
    category_id: Optional[int] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    # Todos opcionales para permitir PATCH parcial
    price: Optional[float] = None
    stock: Optional[int] = None

class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: Optional[CategoryRead] = None