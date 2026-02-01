from fastapi import APIRouter, Header, HTTPException, status
from typing import List
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import OrderService
from app.utils.decorators import measure_time

router = APIRouter()

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
@measure_time
def create_order(payload: OrderCreate, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    # Priority: Idempotency-Key header if present, otherwise payload.request_id
    request_key = idempotency_key or payload.request_id
    try:
        order, created = OrderService.create_order(payload.report, [it.model_dump() for it in payload.items], request_key=request_key)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # If it was idempotent, return 200 OK
    # If created, return 201 (via decorator status_code)
    return order

@router.get("/", response_model=List[OrderRead])
@measure_time
def list_orders():
    """
    Retrieve all service orders.
    """
    orders = OrderService.list_orders()
    return orders
