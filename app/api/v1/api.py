from fastapi import APIRouter
from app.api.v1.endpoints import items, orders, categories, s3

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(s3.router, prefix="/s3", tags=["s3"])