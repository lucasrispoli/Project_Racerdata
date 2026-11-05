from typing import Optional, List
from sqlalchemy.orm import Session
from entity.models import Driver as DriverModel
from repository.driver_repository import DriverRepository
from dto.models_dto import DriverCreateDto, DriverUpdateDto, DriverDto


class DriverService:
    def __init__(self, session: Session):
        self._repository = DriverRepository(session)

    def create(self, dto: DriverCreateDto) -> DriverDto:
        name = dto.driver_name.strip()
        existing = self._repository.get_by_name(name)
        if existing:
            raise ValueError(f"Driver '{name}' already exists.")

        entity = DriverModel(driver_name=name)
        saved = self._repository.create(entity)
        return DriverDto.model_validate(saved)

    def get_by_id(self, driver_id: str) -> Optional[DriverDto]:
        entity = self._repository.get_by_id(driver_id)
        if not entity:
            return None
        return DriverDto.model_validate(entity)

    def get_by_name(self, driver_name: str) -> Optional[DriverDto]:
        entity = self._repository.get_by_name(driver_name)
        if not entity:
            return None
        return DriverDto.model_validate(entity)

    def get_all(self, filter_text: Optional[str] = None) -> List[DriverDto]:
        entities = self._repository.get_all(filter_text=filter_text)
        return [DriverDto.model_validate(e) for e in entities]

    def update(self, driver_id: str, dto: DriverUpdateDto) -> Optional[DriverDto]:
        entity = self._repository.get_by_id(driver_id)
        if not entity:
            return None

        name = dto.driver_name.strip()
        existing = self._repository.get_by_name(name)
        if existing and str(existing.id) != str(entity.id):
            raise ValueError(f"Driver '{name}' already exists.")

        entity.driver_name = name
        updated = self._repository.update(entity)
        return DriverDto.model_validate(updated)

    def delete(self, driver_id: str) -> bool:
        entity = self._repository.get_by_id(driver_id)
        if not entity:
            return False
        return self._repository.delete(entity)
