from fastapi import APIRouter, Header, HTTPException, status, Request
from typing import List
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import OrderService
from app.utils.decorators import measure_time

router = APIRouter()

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
@measure_time
def create_order(payload: OrderCreate, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    # Prioridad: header Idempotency-Key si existe, sino payload.request_id
    request_key = idempotency_key or payload.request_id
    try:
        order, created = OrderService.create_order(payload.report, [it.dict() for it in payload.items], request_key=request_key)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    # Si no se creó ahora (fue idempotente), devolver 200 OK
    # Si se creó, devolver 201 (por el status_code del decorador)
    return order

@router.get("/", response_model=List[OrderRead])
@measure_time
def list_orders():
    """
    Obtiene todas las órdenes de servicio.
    """
    orders = OrderService.list_orders()
    return orders