import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from config.database import Base


class Session(Base):
    """
    1.1 Session: Armazena as sessões disponibilizadas pela OpenF1
    """
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


class Driver(Base):
    """
    1.2 Driver: Cadastro principal e único dos pilotos
    """
    __tablename__ = "driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_name = Column(String(100), unique=True, nullable=False, index=True)

    session_drivers = relationship("SessionDriver", back_populates="driver", cascade="all, delete-orphan")
    dashboard_driver = relationship("DashboardDriver", back_populates="driver", uselist=False, cascade="all, delete-orphan")


class SessionDriver(Base):
    """
    1.3 SessionDriver: Entidade associativa entre Session e Driver
    """
    __tablename__ = "session_driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("session.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(String(36), ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)
    car_number = Column(Integer, nullable=True)
    team_name = Column(String(100), nullable=True)

    session = relationship("Session", back_populates="session_drivers")
    driver = relationship("Driver", back_populates="session_drivers")

    __table_args__ = (
        UniqueConstraint("session_id", "driver_id", name="uq_session_driver"),
    )


class DashboardDriver(Base):
    """
    1.4 DashboardDriver: Configuração personalizada do piloto exibida no Dashboard
    """
    __tablename__ = "dashboard_driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(String(36), ForeignKey("driver.id", ondelete="CASCADE"), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    tag_color = Column(String(30), nullable=True, default="#E10600")
    isActive = Column(Boolean, nullable=False, default=True)

    driver = relationship("Driver", back_populates="dashboard_driver")
