from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from dto.driver_dto import DriverDto
from service.driver_service import DriverService

router = APIRouter(prefix="/drivers", tags=["Drivers"])


def get_service(db: Session = Depends(get_db)) -> DriverService:
    return DriverService(db)


@router.get("/{driver_id}", response_model=DriverDto)
def get_by_id(driver_id: str, service: DriverService = Depends(get_service)):
    return service.get_by_id(driver_id)


@router.get("", response_model=List[DriverDto])
def get_all(
    filter: Optional[str] = Query(None),
    service: DriverService = Depends(get_service)
):
    return service.get_all(filter_text=filter)
