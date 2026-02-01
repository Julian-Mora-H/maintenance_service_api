from typing import List, Dict, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.session import SessionLocal

class OrderService:

    @staticmethod
    def create_order(report: str, items_payload: List[Dict], request_key: Optional[str] = None) -> Tuple[object, bool]:
        
        session = SessionLocal()
        try:
            # Local imports to avoid import cycles
            from app.models.order import Order, order_items
            from app.models.item import Item
            from app.models.idempotency import IdempotencyKey

            # Check previous idempotency
            if request_key:
                existing = (
                    session.query(IdempotencyKey)
                    .filter_by(request_key=request_key, resource_type="order")
                    .first()
                )
                if existing and existing.resource_id:
                    # Return existing order without creating a new one
                    existing_order = session.get(Order, existing.resource_id)
                    # Fetch order items
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
                # Create order
                order = Order(report=report)
                session.add(order)
                session.flush()  # gets order.id

                # Link items (association table)
                for it in items_payload:
                    item_id = it.get("item_id")
                    qty = it.get("quantity", 1)
                    item = session.get(Item, item_id)
                    if item is None:
                        # Raising triggers a rollback
                        raise ValueError(f"Item {item_id} not found")
                    # Insert into order_items table
                    session.execute(
                        order_items.insert().values(order_id=order.id, item_id=item.id, quantity=qty)
                    )

                # Register idempotency key
                if request_key:
                    idemp = IdempotencyKey(
                        request_key=request_key, resource_type="order", resource_id=order.id
                    )
                    session.add(idemp)

                # Commit transaction
                session.commit()
                session.refresh(order)
                # Fetch order items
                from sqlalchemy import select
                items_query = session.execute(
                    select(order_items).where(order_items.c.order_id == order.id)
                ).fetchall()
                
                # Convert to dict while the session is open
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
                # Can happen if concurrent requests insert the same idempotency key
                session.rollback()
                if request_key:
                    existing = (
                        session.query(IdempotencyKey)
                        .filter_by(request_key=request_key, resource_type="order")
                        .first()
                    )
                    if existing and existing.resource_id:
                        existing_order = session.get(Order, existing.resource_id)
                        # Fetch order items
                        from sqlalchemy import select
                        items_query = session.execute(
                            select(order_items).where(order_items.c.order_id == existing_order.id)
                        ).fetchall()
                        # Convert to dict
                        result = {
                            "id": existing_order.id,
                            "report": existing_order.report,
                            "items": [
                                {"item_id": row.item_id, "quantity": row.quantity}
                                for row in items_query
                            ]
                        }
                        return result, False
                # If not idempotency-related, re-raise
                raise ie

        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_order(order_id: int) -> Optional[object]:
        """
        Retrieve an order by id (returns ORM object or None).
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
        List all orders with their items.
        """
        session = SessionLocal()
        try:
            from app.models.order import Order, order_items
            from sqlalchemy import select
            
            orders = session.query(Order).all()
            
            # Convert to list of dicts while the session is open
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