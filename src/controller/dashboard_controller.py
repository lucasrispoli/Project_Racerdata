from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.dashboard_dto import (
    CollectDataSummaryDto,
    DashboardFilterDto,
    DashboardOverviewDto,
)
from dto.session_dto import SessionDto
from dto.session_driver_dto import SessionDriverDto
from service.dashboard_service import DashboardService
from service.collect_service import DataCollectionService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)


@router.post("/collect-data", response_model=CollectDataSummaryDto, status_code=status.HTTP_200_OK)
def collect_data(
    year: Optional[int] = Query(None, description="Ano das sessões para importar da OpenF1"),
    service: DataCollectionService = Depends(get_service)
):
    return service.collect_data(year=year)


@router.get("/overview", response_model=DashboardOverviewDto)
def get_dashboard_overview(
    year: Optional[int] = Query(None),
    session_type: Optional[str] = Query(None),
    team_name: Optional[str] = Query(None),
    service: DashboardService = Depends(get_service)
):
    filters = DashboardFilterDto(year=year, session_type=session_type, team_name=team_name)
    return service.get_overview(filters)


@router.get("/sessions", response_model=List[SessionDto])
def get_dashboard_sessions(
    year: Optional[int] = Query(None),
    session_type: Optional[str] = Query(None),
    service: DashboardService = Depends(get_service)
):
    filters = DashboardFilterDto(year=year, session_type=session_type)
    return service.get_sessions_table(filters)


@router.get("/sessions/{session_id}/participants", response_model=List[SessionDriverDto])
def get_session_participants(
    session_id: str,
    service: DashboardService = Depends(get_service)
):
    return service.get_session_participants(session_id)
