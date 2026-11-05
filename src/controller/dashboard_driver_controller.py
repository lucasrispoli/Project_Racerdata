from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.models_dto import (
    DashboardDriverInputDto,
    DashboardDriverUpdateDto,
    DashboardDriverStatusDto,
    DashboardDriverDto,
)
from service.dashboard_driver_service import DashboardDriverService

# Mantém o prefixo /drivers para compatibilidade com o frontend existente, e também expõe /dashboard-drivers
router = APIRouter(prefix="/drivers", tags=["Dashboard Drivers"])
alias_router = APIRouter(prefix="/dashboard-drivers", tags=["Dashboard Drivers Alias"])


def get_service(db: Session = Depends(get_db)) -> DashboardDriverService:
    return DashboardDriverService(db)


@router.post("", response_model=DashboardDriverDto, status_code=status.HTTP_201_CREATED)
@alias_router.post("", response_model=DashboardDriverDto, status_code=status.HTTP_201_CREATED)
def create_dashboard_driver(dto: DashboardDriverInputDto, service: DashboardDriverService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[DashboardDriverDto])
@alias_router.get("", response_model=List[DashboardDriverDto])
def get_all_dashboard_drivers(
    filter: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    service: DashboardDriverService = Depends(get_service)
):
    return service.get_all(is_active=is_active, filter_text=filter)


@router.get("/{driver_id}", response_model=DashboardDriverDto)
@alias_router.get("/{driver_id}", response_model=DashboardDriverDto)
def get_dashboard_driver_by_id(driver_id: str, service: DashboardDriverService = Depends(get_service)):
    dto = service.get_by_id(driver_id)
    if not dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DashboardDriver not found")
    return dto


@router.put("/{driver_id}", response_model=DashboardDriverDto)
@alias_router.put("/{driver_id}", response_model=DashboardDriverDto)
def update_dashboard_driver(
    driver_id: str,
    dto: DashboardDriverInputDto,
    service: DashboardDriverService = Depends(get_service)
):
    try:
        updated = service.update(driver_id, dto)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DashboardDriver not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{driver_id}/status", response_model=DashboardDriverDto)
@alias_router.patch("/{driver_id}/status", response_model=DashboardDriverDto)
def change_dashboard_driver_status(
    driver_id: str,
    status_dto: DashboardDriverStatusDto,
    service: DashboardDriverService = Depends(get_service)
):
    active_val = status_dto.isActive if status_dto.status is None else status_dto.status
    if active_val is None:
        active_val = True
    updated = service.change_status(driver_id, active_val)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DashboardDriver not found")
    return updated


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
@alias_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dashboard_driver(driver_id: str, service: DashboardDriverService = Depends(get_service)):
    deleted = service.delete(driver_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DashboardDriver not found")
    return None
