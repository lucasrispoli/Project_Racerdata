from typing import Optional, List
from sqlalchemy.orm import Session
from entity.models import Session as SessionModel
from repository.session_repository import SessionRepository
from dto.models_dto import SessionCreateDto, SessionUpdateDto, SessionDto


class SessionService:
    def __init__(self, session: Session):
        self._repository = SessionRepository(session)

    def create(self, dto: SessionCreateDto) -> SessionDto:
        existing = self._repository.get_by_session_key(dto.session_key)
        if existing:
            raise ValueError(f"Session with session_key {dto.session_key} already exists.")

        entity = SessionModel(
            session_key=dto.session_key,
            meeting_key=dto.meeting_key,
            session_name=dto.session_name,
            session_type=dto.session_type,
            year=dto.year,
            country_name=dto.country_name,
            location=dto.location,
            circuit_short_name=dto.circuit_short_name,
            date_start=dto.date_start,
            date_end=dto.date_end,
            is_cancelled=dto.is_cancelled,
        )
        saved = self._repository.create(entity)
        return SessionDto.model_validate(saved)

    def get_by_id(self, session_id: str) -> Optional[SessionDto]:
        entity = self._repository.get_by_id(session_id)
        if not entity:
            return None
        return SessionDto.model_validate(entity)

    def get_all(
        self,
        year: Optional[int] = None,
        session_type: Optional[str] = None,
        country_name: Optional[str] = None,
    ) -> List[SessionDto]:
        entities = self._repository.get_all(year=year, session_type=session_type, country_name=country_name)
        return [SessionDto.model_validate(e) for e in entities]

    def update(self, session_id: str, dto: SessionUpdateDto) -> Optional[SessionDto]:
        entity = self._repository.get_by_id(session_id)
        if not entity:
            return None

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(entity, field, value)

        updated = self._repository.update(entity)
        return SessionDto.model_validate(updated)

    def delete(self, session_id: str) -> bool:
        entity = self._repository.get_by_id(session_id)
        if not entity:
            return False
        return self._repository.delete(entity)
