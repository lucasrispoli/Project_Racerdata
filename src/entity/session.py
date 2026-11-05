import uuid
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from config.database import Base


class Session(Base):
  
    __tablename__ = "session"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_key = Column(Integer, unique=True, nullable=False, index=True)
    meeting_key = Column(Integer, nullable=True)
    session_name = Column(String(100), nullable=True)
    session_type = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True, index=True)
    country_name = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    circuit_short_name = Column(String(100), nullable=True)
    date_start = Column(String(35), nullable=True)
    date_end = Column(String(35), nullable=True)
    is_cancelled = Column(Boolean, default=False)

    session_drivers = relationship("SessionDriver", back_populates="session", cascade="all, delete-orphan")
