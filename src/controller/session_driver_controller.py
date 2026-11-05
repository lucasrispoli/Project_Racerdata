from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.models_dto import SessionDriverCreateDto, SessionDriverUpdateDto, SessionDriverDto
from service.session_driver_service import SessionDriverService

router = APIRouter(prefix="/session-drivers", tags=["Session Drivers"])


def get_service(db: Session = Depends(get_db)) -> SessionDriverService:
    return SessionDriverService(db)


@router.post("", response_model=SessionDriverDto, status_code=status.HTTP_201_CREATED)
def create_session_driver(dto: SessionDriverCreateDto, service: SessionDriverService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[SessionDriverDto])
def get_all_session_drivers(
    year: Optional[int] = Query(None),
    driver_id: Optional[str] = Query(None),
    team_name: Optional[str] = Query(None),
    service: SessionDriverService = Depends(get_service)
):
    return service.get_all(year=year, driver_id=driver_id, team_name=team_name)


@router.get("/{session_driver_id}", response_model=SessionDriverDto)
def get_session_driver_by_id(session_driver_id: str, service: SessionDriverService = Depends(get_service)):
    dto = service.get_by_id(session_driver_id)
    if not dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SessionDriver not found")
    return dto


@router.put("/{session_driver_id}", response_model=SessionDriverDto)
def update_session_driver(session_driver_id: str, dto: SessionDriverUpdateDto, service: SessionDriverService = Depends(get_service)):
    updated = service.update(session_driver_id, dto)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SessionDriver not found")
    return updated


@router.delete("/{session_driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session_driver(session_driver_id: str, service: SessionDriverService = Depends(get_service)):
    deleted = service.delete(session_driver_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SessionDriver not found")
    return None
