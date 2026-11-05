from typing import Optional, List
from sqlalchemy.orm import Session
from entity.dashboard_driver import DashboardDriver as DashboardDriverModel
from entity.driver import Driver as DriverModel
from repository.dashboard_driver_repository import DashboardDriverRepository
from repository.driver_repository import DriverRepository
from dto.dashboard_driver_dto import (
    DashboardDriverInputDto,
    DashboardDriverUpdateDto,
    DashboardDriverStatusDto,
    DashboardDriverDto,
)


class DashboardDriverService:
    def __init__(self, session: Session):
        self._repository = DashboardDriverRepository(session)
        self._driver_repo = DriverRepository(session)

    def create(self, dto: DashboardDriverInputDto) -> DashboardDriverDto:
        driver_id = dto.driver_id
        driver_name = (dto.driver_name or dto.name or "").strip()

        if not driver_id:
            if not driver_name:
                raise ValueError("Driver name or driver ID is required.")
            driver_obj = self._driver_repo.get_by_name(driver_name)
            if not driver_obj:
                driver_obj = self._driver_repo.create(DriverModel(driver_name=driver_name))
            driver_id = str(driver_obj.id)
        else:
            driver_obj = self._driver_repo.get_by_id(driver_id)
            if not driver_obj:
                raise ValueError(f"Driver with id '{driver_id}' not found.")

        existing = self._repository.get_by_driver_id(driver_id)
        if existing:
            raise ValueError(f"Dashboard configuration for driver '{driver_obj.driver_name}' already exists.")

        is_active_val = dto.isActive if dto.status is None else dto.status

        entity = DashboardDriverModel(
            driver_id=driver_id,
            description=dto.description or "",
            tag_color=dto.tag_color or "#E10600",
            isActive=is_active_val,
        )
        saved = self._repository.create(entity)
        return DashboardDriverDto.from_entity(saved)

    def get_by_id(self, dashboard_driver_id: str) -> Optional[DashboardDriverDto]:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            return None
        return DashboardDriverDto.from_entity(entity)

    def get_all(
        self,
        is_active: Optional[bool] = None,
        filter_text: Optional[str] = None
    ) -> List[DashboardDriverDto]:
        entities = self._repository.get_all(is_active=is_active, filter_text=filter_text)
        return [DashboardDriverDto.from_entity(e) for e in entities]

    def update(self, dashboard_driver_id: str, dto: DashboardDriverUpdateDto | DashboardDriverInputDto) -> Optional[DashboardDriverDto]:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            return None

        name_val = getattr(dto, "driver_name", None) or getattr(dto, "name", None)
        if name_val and entity.driver:
            name_val = name_val.strip()
            existing_driver = self._driver_repo.get_by_name(name_val)
            if existing_driver and str(existing_driver.id) != str(entity.driver.id):
                raise ValueError(f"Driver '{name_val}' already exists.")
            entity.driver.driver_name = name_val

        if dto.description is not None:
            entity.description = dto.description

        if getattr(dto, "tag_color", None) is not None:
            entity.tag_color = dto.tag_color

        status_val = getattr(dto, "status", None)
        if status_val is not None:
            entity.isActive = status_val
        elif getattr(dto, "isActive", None) is not None:
            entity.isActive = dto.isActive

        updated = self._repository.update(entity)
        return DashboardDriverDto.from_entity(updated)

    def change_status(self, dashboard_driver_id: str, is_active: bool) -> Optional[DashboardDriverDto]:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            return None
        entity.isActive = is_active
        updated = self._repository.update(entity)
        return DashboardDriverDto.from_entity(updated)

    def delete(self, dashboard_driver_id: str) -> bool:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            return False
        return self._repository.delete(entity)
