from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.models_dto import DriverCreateDto, DriverUpdateDto, DriverDto
from service.driver_service import DriverService

router = APIRouter(prefix="/driver-entities", tags=["Driver Entities"])


def get_service(db: Session = Depends(get_db)) -> DriverService:
    return DriverService(db)


@router.post("", response_model=DriverDto, status_code=status.HTTP_201_CREATED)
def create_driver(dto: DriverCreateDto, service: DriverService = Depends(get_service)):
    try:
        return service.create(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[DriverDto])
def get_all_drivers(
    filter: Optional[str] = Query(None),
    service: DriverService = Depends(get_service)
):
    return service.get_all(filter_text=filter)


@router.get("/{driver_id}", response_model=DriverDto)
def get_driver_by_id(driver_id: str, service: DriverService = Depends(get_service)):
    dto = service.get_by_id(driver_id)
    if not dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return dto


@router.put("/{driver_id}", response_model=DriverDto)
def update_driver(driver_id: str, dto: DriverUpdateDto, service: DriverService = Depends(get_service)):
    try:
        updated = service.update(driver_id, dto)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: str, service: DriverService = Depends(get_service)):
    deleted = service.delete(driver_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return None
