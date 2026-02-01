from typing import List, Dict, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.session import SessionLocal

class OrderService:

    @staticmethod
    def create_order(report: str, items_payload: List[Dict], request_key: Optional[str] = None) -> Tuple[object, bool]:
        
        session = SessionLocal()
        try:
            # import locales para evitar import cycles
            from app.models.order import Order, order_items
            from app.models.item import Item
            from app.models.idempotency import IdempotencyKey

            # Verificar idempotencia previa
            if request_key:
                existing = (
                    session.query(IdempotencyKey)
                    .filter_by(request_key=request_key, resource_type="order")
                    .first()
                )
                if existing and existing.resource_id:
                    # devolver la orden existente sin crear nada
                    existing_order = session.get(Order, existing.resource_id)
                    # Obtener los items de la orden
                    from sqlalchemy import select
                    items_query = session.execute(
                        select(order_items).where(order_items.c.order_id == existing_order.id)
                    ).fetchall()
                    result = {
                        "id": existing_order.id,
                        "report": existing_order.report,
                        "items": [
                            {"item_id": row.item_id, "quantity": row.quantity}
                            for row in items_query
                        ]
                    }
                    return result, False

            try:
                # crear orden
                order = Order(report=report)
                session.add(order)
                session.flush()  # obtiene order.id

                # vincular items (tabla association)
                for it in items_payload:
                    item_id = it.get("item_id")
                    qty = it.get("quantity", 1)
                    item = session.get(Item, item_id)
                    if item is None:
                        # Al lanzar se hará rollback
                        raise ValueError(f"Item {item_id} not found")
                    # insertar en tabla order_items
                    session.execute(
                        order_items.insert().values(order_id=order.id, item_id=item.id, quantity=qty)
                    )

                # Registrar clave de idempotencia
                if request_key:
                    idemp = IdempotencyKey(
                        request_key=request_key, resource_type="order", resource_id=order.id
                    )
                    session.add(idemp)

                # Commit la transacción
                session.commit()
                session.refresh(order)
                # Obtener los items de la orden
                from sqlalchemy import select
                items_query = session.execute(
                    select(order_items).where(order_items.c.order_id == order.id)
                ).fetchall()
                
                # Convertir a dict MIENTRAS la sesión esté abierta
                result = {
                    "id": order.id,
                    "report": order.report,
                    "items": [
                        {"item_id": row.item_id, "quantity": row.quantity}
                        for row in items_query
                    ]
                }
                return result, True

            except IntegrityError as ie:
                # Puede ocurrir si dos peticiones concurrentes intentan insertar la misma idempotency key
                session.rollback()
                if request_key:
                    existing = (
                        session.query(IdempotencyKey)
                        .filter_by(request_key=request_key, resource_type="order")
                        .first()
                    )
                    if existing and existing.resource_id:
                        existing_order = session.get(Order, existing.resource_id)
                        # Obtener los items de la orden
                        from sqlalchemy import select
                        items_query = session.execute(
                            select(order_items).where(order_items.c.order_id == existing_order.id)
                        ).fetchall()
                        # Convertir a dict
                        result = {
                            "id": existing_order.id,
                            "report": existing_order.report,
                            "items": [
                                {"item_id": row.item_id, "quantity": row.quantity}
                                for row in items_query
                            ]
                        }
                        return result, False
                # si no es por idempotencia, propagar
                raise ie

        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_order(order_id: int) -> Optional[object]:
        """
        Recupera una orden por id (devuelve objeto ORM o None).
        """
        session = SessionLocal()
        try:
            from app.models.order import Order
            order = session.get(Order, order_id)
            return order
        finally:
            session.close()

    @staticmethod
    def list_orders():
        """
        Lista todas las órdenes con sus items.
        """
        session = SessionLocal()
        try:
            from app.models.order import Order, order_items
            from sqlalchemy import select
            
            orders = session.query(Order).all()
            
            # Convertir a list de dicts MIENTRAS la sesión esté abierta
            result = []
            for order in orders:
                items_query = session.execute(
                    select(order_items).where(order_items.c.order_id == order.id)
                ).fetchall()
                
                result.append({
                    "id": order.id,
                    "report": order.report,
                    "items": [
                        {"item_id": row.item_id, "quantity": row.quantity}
                        for row in items_query
                    ],
                    "created_at": order.created_at
                })
            
            return result
        finally:
            session.close()