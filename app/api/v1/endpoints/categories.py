from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService
from app.utils.decorators import measure_time

router = APIRouter()

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
@measure_time
def create_category(payload: CategoryCreate):
    category = CategoryService.create_category(payload.model_dump())
    return category

@router.get("/", response_model=List[CategoryRead])
@measure_time
def list_categories():
    categories = CategoryService.list_categories()
    return categories

@router.patch("/{category_id}", response_model=CategoryRead)
@measure_time
def patch_category(category_id: int, payload: CategoryUpdate):
    data = payload.model_dump(exclude_unset=True)
    category = CategoryService.patch_category(category_id, data)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category
