from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.session import Base


# Item model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=False, unique=False, index=False)
    price = Column(Float, nullable=False, default=0.0)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)


    # Relationship with Category table - selectin for eager loading
    category = relationship("Category", back_populates="items", lazy="selectin")

    __table_args__ = (
        Index("ix_items_sku", "sku"),  # Default B-Tree index in most DBs
    )