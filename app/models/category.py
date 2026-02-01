from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship
from app.db.session import Base

# Category model
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

# Relationship with Item table
    items = relationship("Item", back_populates="category")