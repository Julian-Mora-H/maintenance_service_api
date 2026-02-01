from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal

class CategoryService:
    @staticmethod
    def create_category(data) -> dict:
        session = SessionLocal()
        try:
            from app.models.category import Category
            category = Category(**data)
            session.add(category)
            session.commit()
            session.refresh(category)
            # Convertir a dict MIENTRAS la sesión esté abierta
            result = {
                "id": category.id,
                "name": category.name
            }
            return result
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def list_categories():
        session = SessionLocal()
        try:
            from app.models.category import Category
            categories = session.query(Category).all()
            # Convertir a list de dicts mientras la sesión esté abierta
            return [
                {
                    "id": category.id,
                    "name": category.name
                }
                for category in categories
            ]
        finally:
            session.close()

    @staticmethod
    def patch_category(category_id: int, update_data: dict):
        session = SessionLocal()
        try:
            from app.models.category import Category
            category = session.query(Category).filter(Category.id == category_id).first()
            if not category:
                return None
            for key, value in update_data.items():
                if hasattr(category, key) and value is not None:
                    setattr(category, key, value)
            session.commit()
            session.refresh(category)
            # Convertir a dict MIENTRAS la sesión esté abierta
            result = {
                "id": category.id,
                "name": category.name
            }
            return result
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
