from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from dto.dashboard_dto import CollectDataSummaryDto
from service.collect_service import DataCollectionService

router = APIRouter(prefix="/dashboard", tags=["Dashboard / Coleta"])


def get_service(db: Session = Depends(get_db)) -> DataCollectionService:
    return DataCollectionService(db)


@router.post("/collect-data", response_model=CollectDataSummaryDto, status_code=status.HTTP_200_OK)
def collect_data(
    year: Optional[int] = Query(None, description="Ano das sessões para importar da OpenF1"),
    service: DataCollectionService = Depends(get_service)
):
    return service.collect_data(year=year)
