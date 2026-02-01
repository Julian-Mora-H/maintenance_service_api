from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item_service import ItemService
from app.utils.decorators import measure_time

router = APIRouter()

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@measure_time
def create_item(payload: ItemCreate):
    item = ItemService.create_item(payload.model_dump())
    return item

@router.get("/", response_model=List[ItemRead])
@measure_time
def list_items():
    items = ItemService.list_items()
    return items

@router.patch("/{item_id}", response_model=ItemRead)
@measure_time
def patch_item(item_id: int, payload: ItemUpdate):
    data = payload.model_dump(exclude_unset=True)
    item = ItemService.patch_item(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
