from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from dto.session_driver_dto import SessionDriverDto
from dto.session_driver_line_chart_dto import SessionDriverLineChartDto
from dto.session_driver_results_dto import SessionDriverResultsDto
from service.session_driver_service import SessionDriverService

router = APIRouter(prefix="/session-drivers", tags=["Session Drivers"])


def get_service(db: Session = Depends(get_db)) -> SessionDriverService:
    return SessionDriverService(db)


@router.get("/line-chart", response_model=List[SessionDriverLineChartDto])
def get_drivers_for_line_chart(
    date_from: Optional[str] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="Data final no formato YYYY-MM-DD"),
    session_type: Optional[str] = Query(None, description="Tipo de sessao (ex: Race, Qualifying, Practice 1)"),
    service: SessionDriverService = Depends(get_service)
):
    return service.get_drivers_for_line_chart(date_from=date_from, date_to=date_to, session_type=session_type)


@router.get("/results", response_model=List[SessionDriverResultsDto])
def get_all_results(
    year: Optional[int] = Query(None, description="Filtrar por ano da sessao"),
    date_from: Optional[str] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="Data final no formato YYYY-MM-DD"),
    session_type: Optional[str] = Query(None, description="Tipo de sessao (ex: Race, Qualifying, Practice 1)"),
    service: SessionDriverService = Depends(get_service)
):
    return service.get_all_results(year=year, date_from=date_from, date_to=date_to, session_type=session_type)


@router.get("", response_model=List[SessionDriverDto])
def get_all(
    filter_text: Optional[str] = Query(None, description="Filtro por nome de equipe ou piloto"),
    service: SessionDriverService = Depends(get_service)
):
    return service.get_all(filter_text=filter_text)


@router.get("/{session_driver_id}", response_model=SessionDriverDto)
def get_by_id(
    session_driver_id: str,
    service: SessionDriverService = Depends(get_service)
):
    return service.get_by_id(session_driver_id)
