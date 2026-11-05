from typing import Optional, List
from sqlalchemy.orm import Session
from entity.models import SessionDriver as SessionDriverModel
from repository.session_driver_repository import SessionDriverRepository
from repository.session_repository import SessionRepository
from repository.driver_repository import DriverRepository
from dto.models_dto import SessionDriverCreateDto, SessionDriverUpdateDto, SessionDriverDto


class SessionDriverService:
    def __init__(self, session: Session):
        self._repository = SessionDriverRepository(session)
        self._session_repo = SessionRepository(session)
        self._driver_repo = DriverRepository(session)

    def create(self, dto: SessionDriverCreateDto) -> SessionDriverDto:
        session_obj = self._session_repo.get_by_id(dto.session_id)
        if not session_obj:
            raise ValueError(f"Session with id '{dto.session_id}' not found.")

        driver_obj = self._driver_repo.get_by_id(dto.driver_id)
        if not driver_obj:
            raise ValueError(f"Driver with id '{dto.driver_id}' not found.")

        existing = self._repository.get_by_session_and_driver(dto.session_id, dto.driver_id)
        if existing:
            raise ValueError("This driver is already registered in this session.")

        entity = SessionDriverModel(
            session_id=dto.session_id,
            driver_id=dto.driver_id,
            car_number=dto.car_number,
            team_name=dto.team_name,
        )
        saved = self._repository.create(entity)
        return SessionDriverDto.from_entity(saved)

    def get_by_id(self, session_driver_id: str) -> Optional[SessionDriverDto]:
        entity = self._repository.get_by_id(session_driver_id)
        if not entity:
            return None
        return SessionDriverDto.from_entity(entity)

    def get_all(
        self,
        year: Optional[int] = None,
        driver_id: Optional[str] = None,
        team_name: Optional[str] = None,
    ) -> List[SessionDriverDto]:
        entities = self._repository.get_all(year=year, driver_id=driver_id, team_name=team_name)
        return [SessionDriverDto.from_entity(e) for e in entities]

    def update(self, session_driver_id: str, dto: SessionDriverUpdateDto) -> Optional[SessionDriverDto]:
        entity = self._repository.get_by_id(session_driver_id)
        if not entity:
            return None

        if dto.car_number is not None:
            entity.car_number = dto.car_number
        if dto.team_name is not None:
            entity.team_name = dto.team_name

        updated = self._repository.update(entity)
        return SessionDriverDto.from_entity(updated)

    def delete(self, session_driver_id: str) -> bool:
        entity = self._repository.get_by_id(session_driver_id)
        if not entity:
            return False
        return self._repository.delete(entity)
