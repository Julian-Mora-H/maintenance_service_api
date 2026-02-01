from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# tabla de asociación order_items (simplificada)
order_items = Table(
    "order_items",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
)

# modelo Order
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    report = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # relación con la tabla Item a través de la tabla de asociación order_items
    items = relationship("Item", secondary=order_items)