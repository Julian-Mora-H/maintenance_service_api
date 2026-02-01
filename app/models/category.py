from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship
from app.db.session import Base

# modelo Category
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

# relación con la tabla Item
    items = relationship("Item", back_populates="category")