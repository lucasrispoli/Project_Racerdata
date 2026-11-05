from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.dashboard_driver_input_dto import DashboardDriverInputDto
from dto.dashboard_driver_dto import DashboardDriverDto
from service.dashboard_driver_service import DashboardDriverService

router = APIRouter(prefix="/dashboard-drivers", tags=["Dashboard Drivers"])


def get_service(db: Session = Depends(get_db)) -> DashboardDriverService:
    return DashboardDriverService(db)


@router.post("", response_model=DashboardDriverDto, status_code=status.HTTP_201_CREATED)
def create(dto: DashboardDriverInputDto, service: DashboardDriverService = Depends(get_service)):
    return service.create(dto)


@router.put("/{dashboard_driver_id}", response_model=DashboardDriverDto)
def update(
    dashboard_driver_id: str,
    dto: DashboardDriverInputDto,
    service: DashboardDriverService = Depends(get_service)
):
    return service.update(dashboard_driver_id, dto)


@router.delete("/{dashboard_driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(dashboard_driver_id: str, service: DashboardDriverService = Depends(get_service)):
    service.delete(dashboard_driver_id)
    return None


@router.get("/{dashboard_driver_id}", response_model=DashboardDriverDto)
def get_by_id(dashboard_driver_id: str, service: DashboardDriverService = Depends(get_service)):
    return service.get_by_id(dashboard_driver_id)


@router.get("", response_model=List[DashboardDriverDto])
def get_all(
    filter: Optional[str] = Query(None),
    service: DashboardDriverService = Depends(get_service)
):
    return service.get_all(filter_text=filter)


@router.patch("/{dashboard_driver_id}/status", response_model=DashboardDriverDto)
def change_status(
    dashboard_driver_id: str,
    isActive: bool = Query(...),
    service: DashboardDriverService = Depends(get_service)
):
    return service.change_status(dashboard_driver_id, isActive)
