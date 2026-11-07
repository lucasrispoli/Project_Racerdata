from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repository.session_repository import SessionRepository
from dto.session_dto import SessionDto


class SessionService:
    def __init__(self, session: Session):
        self._repository = SessionRepository(session)

    def get_by_id(self, session_id: str) -> SessionDto:
        entity = self._repository.get_by_id(session_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sessão não encontrada."
            )
        return SessionDto.from_entity(entity)

    def get_all(self, filter_text: Optional[str] = None) -> List[SessionDto]:
        entities = self._repository.get_all(filter_text=filter_text)
        return [SessionDto.from_entity(e) for e in entities]

    def get_by_year(self, year: int) -> List[SessionDto]:
        entities = self._repository.get_by_year(year)
        return [SessionDto.from_entity(e) for e in entities]

    def get_by_session_code(self, session_key: int) -> SessionDto:
        entity = self._repository.get_by_session_key(session_key)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sessão com session_key '{session_key}' não encontrada."
            )
        return SessionDto.from_entity(entity)

    def get_by_session_type(self, session_type: str) -> List[SessionDto]:
        entities = self._repository.get_by_session_type(session_type)
        return [SessionDto.from_entity(e) for e in entities]
