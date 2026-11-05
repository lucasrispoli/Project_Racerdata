from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# DRIVER DTOs
# ==========================================
class DriverCreateDto(BaseModel):
    driver_name: str


class DriverUpdateDto(BaseModel):
    driver_name: str


class DriverDto(BaseModel):
    id: str
    driver_name: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# DASHBOARD DRIVER DTOs (Configuração visual/ativação)
# ==========================================
class DashboardDriverInputDto(BaseModel):
    driver_name: Optional[str] = None  # Se informado, pode criar o Driver se não existir ou associar
    driver_id: Optional[str] = None
    description: Optional[str] = ""
    tag_color: Optional[str] = "#E10600"
    isActive: bool = True
    name: Optional[str] = None  # Retrocompatibilidade com frontend anterior
    status: Optional[bool] = None  # Retrocompatibilidade com frontend anterior


class DashboardDriverUpdateDto(BaseModel):
    description: Optional[str] = None
    tag_color: Optional[str] = None
    isActive: Optional[bool] = None
    status: Optional[bool] = None  # Retrocompatibilidade


class DashboardDriverStatusDto(BaseModel):
    isActive: Optional[bool] = None
    status: Optional[bool] = None  # Retrocompatibilidade


class DashboardDriverDto(BaseModel):
    id: str
    driver_id: str
    driver_name: str
    description: str
    tag_color: str
    isActive: bool

    # Campos de compatibilidade para a UI existente
    name: str = ""
    status: bool = True

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "DashboardDriverDto":
        driver_name = entity.driver.driver_name if entity.driver else ""
        return cls(
            id=str(entity.id),
            driver_id=str(entity.driver_id),
            driver_name=driver_name,
            description=entity.description or "",
            tag_color=entity.tag_color or "#E10600",
            isActive=bool(entity.isActive),
            name=driver_name,
            status=bool(entity.isActive),
        )


# ==========================================
# SESSION DTOs
# ==========================================
class SessionCreateDto(BaseModel):
    session_key: int
    meeting_key: Optional[int] = None
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: bool = False


class SessionUpdateDto(BaseModel):
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: Optional[bool] = None


class SessionDto(BaseModel):
    id: str
    session_key: int
    meeting_key: Optional[int] = None
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: bool = False

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SESSION DRIVER DTOs
# ==========================================
class SessionDriverCreateDto(BaseModel):
    session_id: str
    driver_id: str
    car_number: Optional[int] = None
    team_name: Optional[str] = None


class SessionDriverUpdateDto(BaseModel):
    car_number: Optional[int] = None
    team_name: Optional[str] = None


class SessionDriverDto(BaseModel):
    id: str
    session_id: str
    driver_id: str
    driver_name: Optional[str] = None
    session_name: Optional[str] = None
    car_number: Optional[int] = None
    team_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity) -> "SessionDriverDto":
        return cls(
            id=str(entity.id),
            session_id=str(entity.session_id),
            driver_id=str(entity.driver_id),
            driver_name=entity.driver.driver_name if entity.driver else None,
            session_name=entity.session.session_name if entity.session else None,
            car_number=entity.car_number,
            team_name=entity.team_name,
        )


# ==========================================
# DASHBOARD SERVICE & ANALYTICS DTOs
# ==========================================
class CollectDataSummaryDto(BaseModel):
    sessions_found: int = 0
    sessions_new: int = 0
    sessions_updated: int = 0
    drivers_found: int = 0
    drivers_new: int = 0
    participations_created: int = 0
    participations_updated: int = 0
    errors_count: int = 0
    failed_sessions: List[int] = Field(default_factory=list)


class DashboardFilterDto(BaseModel):
    year: Optional[int] = None
    session_type: Optional[str] = None
    driver_id: Optional[str] = None
    team_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class PerformancePointDto(BaseModel):
    session_name: str
    session_date: str
    car_number: Optional[int] = None
    team_name: Optional[str] = None
    value: float | int | None = None


class DriverPerformanceDto(BaseModel):
    driver_id: str
    driver_name: str
    tag_color: str
    points: List[PerformancePointDto]


class DashboardOverviewDto(BaseModel):
    total_sessions: int
    total_drivers: int
    active_dashboard_drivers: int
    available_years: List[int]
    drivers_performance: List[DriverPerformanceDto]
