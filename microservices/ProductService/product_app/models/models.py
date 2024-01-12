from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db.database import Base


class Products(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String)
    weight = Column(Float)
    description = Column(String)
