from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal

class ItemService:
    @staticmethod
    def create_item(data) -> object:
        session = SessionLocal()
        try:
            # importar aquí evita ciclos en la importación de módulos
            from app.models.item import Item
            item = Item(**data)
            session.add(item)
            session.commit()
            session.refresh(item)
            # Convertir a dict MIENTRAS la sesión esté abierta
            result = {
                "id": item.id,
                "name": item.name,
                "sku": item.sku,
                "price": item.price,
                "stock": item.stock,
                "category_id": item.category_id,
                "category": {
                    "id": item.category.id,
                    "name": item.category.name
                } if item.category else None
            }
            return result
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def list_items():
        session = SessionLocal()
        try:
            from app.models.item import Item
            from app.models.category import Category
            # LEFT JOIN explícito
            items = session.query(Item).outerjoin(Category).all()
            # Convertir a dict mientras la sesión esté abierta
            return [
                {
                    "id": item.id,
                    "name": item.name,
                    "sku": item.sku,
                    "price": item.price,
                    "stock": item.stock,
                    "category_id": item.category_id,
                    "category": {
                        "id": item.category.id,
                        "name": item.category.name
                    } if item.category else None
                }
                for item in items
            ]
        finally:
            session.close()

    @staticmethod
    def patch_item(item_id: int, update_data: dict):
        session = SessionLocal()
        try:
            from app.models.item import Item
            item = session.query(Item).filter(Item.id == item_id).first()
            if not item:
                return None
            for key, value in update_data.items():
                if hasattr(item, key) and value is not None:
                    setattr(item, key, value)
            session.commit()
            session.refresh(item)
            # Convertir a dict MIENTRAS la sesión esté abierta
            result = {
                "id": item.id,
                "name": item.name,
                "sku": item.sku,
                "price": item.price,
                "stock": item.stock,
                "category_id": item.category_id,
                "category": {
                    "id": item.category.id,
                    "name": item.category.name
                } if item.category else None
            }
            return result
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()