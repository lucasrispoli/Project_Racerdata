from typing import Optional
from pydantic import BaseModel, ConfigDict


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
