import uuid
from sqlalchemy import Column, String, Boolean, Text
from config.database import Base


class Driver(Base):
    __tablename__ = "driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Driver(id='{self.id}', name='{self.name}', active={self.active})>"
