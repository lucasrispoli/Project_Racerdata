from typing import Optional
from pydantic import BaseModel, ConfigDict


class DashboardDriverInputDto(BaseModel):
    driver_name: Optional[str] = None
    driver_id: Optional[str] = None
    description: Optional[str] = ""
    tag_color: Optional[str] = "#E10600"
    isActive: bool = True
    name: Optional[str] = None
    status: Optional[bool] = None


class DashboardDriverUpdateDto(BaseModel):
    description: Optional[str] = None
    tag_color: Optional[str] = None
    isActive: Optional[bool] = None
    status: Optional[bool] = None


class DashboardDriverStatusDto(BaseModel):
    isActive: Optional[bool] = None
    status: Optional[bool] = None


class DashboardDriverDto(BaseModel):
    id: str
    driver_id: str
    driver_name: str
    description: str
    tag_color: str
    isActive: bool

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
