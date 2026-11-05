from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from dto.session_dto import SessionDto
from service.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_service(db: Session = Depends(get_db)) -> SessionService:
    return SessionService(db)


@router.get("/by-year/{year}", response_model=List[SessionDto])
def get_by_year(year: int, service: SessionService = Depends(get_service)):
    return service.get_by_year(year)


@router.get("/by-session-code/{session_key}", response_model=SessionDto)
def get_by_session_code(session_key: int, service: SessionService = Depends(get_service)):
    return service.get_by_session_code(session_key)


@router.get("/by-session-type/{session_type}", response_model=List[SessionDto])
def get_by_session_type(session_type: str, service: SessionService = Depends(get_service)):
    return service.get_by_session_type(session_type)


@router.get("/{session_id}", response_model=SessionDto)
def get_by_id(session_id: str, service: SessionService = Depends(get_service)):
    return service.get_by_id(session_id)


@router.get("", response_model=List[SessionDto])
def get_all(
    filter: Optional[str] = Query(None),
    service: SessionService = Depends(get_service)
):
    return service.get_all(filter_text=filter)
