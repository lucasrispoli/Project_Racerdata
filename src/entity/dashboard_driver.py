import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class DashboardDriver(Base):

    __tablename__ = "dashboard_driver"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(String(36), ForeignKey("driver.id", ondelete="CASCADE"), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    tag_color = Column(String(30), nullable=True, default="#E10600")
    # Mapeia explicitamente para o nome da coluna física minúscula no PostgreSQL 'isactive'
    # mantendo o atributo Python .isActive para manter compatibilidade com DTOs e regras de negócio
    isActive = Column("isactive", Boolean, nullable=False, default=True)

    driver = relationship("Driver", back_populates="dashboard_driver")
