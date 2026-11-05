from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.models_dto import SessionCreateDto, SessionUpdateDto, SessionDto
from service.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_service(db: Session = Depends(get_db)) -> SessionService:
    return SessionService(db)


@router.post("", response_model=SessionDto, status_code=status.HTTP_201_CREATED)
def create_session(dto: SessionCreateDto, service: SessionService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[SessionDto])
def get_all_sessions(
    year: Optional[int] = Query(None),
    session_type: Optional[str] = Query(None),
    country_name: Optional[str] = Query(None),
    service: SessionService = Depends(get_service)
):
    return service.get_all(year=year, session_type=session_type, country_name=country_name)


@router.get("/{session_id}", response_model=SessionDto)
def get_session_by_id(session_id: str, service: SessionService = Depends(get_service)):
    dto = service.get_by_id(session_id)
    if not dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return dto


@router.put("/{session_id}", response_model=SessionDto)
def update_session(session_id: str, dto: SessionUpdateDto, service: SessionService = Depends(get_service)):
    updated = service.update(session_id, dto)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return updated


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, service: SessionService = Depends(get_service)):
    deleted = service.delete(session_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return None
