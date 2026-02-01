from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# order_items association table (simplified)
order_items = Table(
    "order_items",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
)

# Order model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    report = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # Relationship with Item table through order_items association table
    items = relationship("Item", secondary=order_items)