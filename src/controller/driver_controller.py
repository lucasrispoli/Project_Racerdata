from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.driver_dto import DriverDto, DriverInputDto, DriverStatusUpdateDto
from service.driver_service import DriverService

router = APIRouter(prefix="/drivers", tags=["Drivers"])


def get_driver_service(db: Session = Depends(get_db)) -> DriverService:
    return DriverService(db)


@router.post("", response_model=DriverDto, status_code=status.HTTP_201_CREATED)
def create_driver(input_dto: DriverInputDto, service: DriverService = Depends(get_driver_service)):
    try:
        return service.create(input_dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[DriverDto])
def get_all_drivers(
    filter: Optional[str] = Query(None),
    service: DriverService = Depends(get_driver_service)
):
    return service.get_all(filter_text=filter)


@router.get("/{driver_id}", response_model=DriverDto)
def get_driver_by_id(driver_id: str, service: DriverService = Depends(get_driver_service)):
    driver_dto = service.get_by_id(driver_id)
    if not driver_dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return driver_dto


@router.put("/{driver_id}", response_model=DriverDto)
def update_driver(
    driver_id: str,
    input_dto: DriverInputDto,
    service: DriverService = Depends(get_driver_service)
):
    try:
        updated = service.update(driver_id, input_dto)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{driver_id}/status", response_model=DriverDto)
def change_driver_status(
    driver_id: str,
    status_dto: DriverStatusUpdateDto,
    service: DriverService = Depends(get_driver_service)
):
    updated = service.change_status(driver_id, status_dto.status)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return updated


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: str, service: DriverService = Depends(get_driver_service)):
    deleted = service.delete(driver_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return None
