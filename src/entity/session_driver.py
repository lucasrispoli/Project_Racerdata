import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from config.database import Base


class SessionDriver(Base):

    __tablename__ = "session_driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("session.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(String(36), ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)
    car_number = Column(Integer, nullable=True)
    driver_position = Column(Integer, nullable=True)
    team_name = Column(String(100), nullable=True)

    session = relationship("Session", back_populates="session_drivers")
    driver = relationship("Driver", back_populates="session_drivers")

    __table_args__ = (
        UniqueConstraint("session_id", "driver_id", name="uq_session_driver"),
    )
