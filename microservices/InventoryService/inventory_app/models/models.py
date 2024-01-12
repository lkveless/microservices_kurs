from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    product_name = Column(String)
    quantity_on_inventory = Column(Float)
    current_price = Column(Float)
