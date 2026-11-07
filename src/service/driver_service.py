from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repository.driver_repository import DriverRepository
from dto.driver_dto import DriverDto


class DriverService:
    def __init__(self, session: Session):
        self._repository = DriverRepository(session)

    def get_by_id(self, driver_id: str) -> DriverDto:
        entity = self._repository.get_by_id(driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Piloto não encontrado."
            )
        return DriverDto.from_entity(entity)

    def get_all(self, filter_text: Optional[str] = None) -> List[DriverDto]:
        entities = self._repository.get_all(filter_text=filter_text)
        return [DriverDto.from_entity(e) for e in entities]
