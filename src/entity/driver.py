import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from config.database import Base


class Driver(Base):
 
    __tablename__ = "driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_name = Column(String(100), unique=True, nullable=False, index=True)

    session_drivers = relationship("SessionDriver", back_populates="driver", cascade="all, delete-orphan")
    dashboard_driver = relationship("DashboardDriver", back_populates="driver", uselist=False, cascade="all, delete-orphan")
