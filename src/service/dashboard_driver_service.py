from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from entity.dashboard_driver import DashboardDriver as DashboardDriverModel
from repository.dashboard_driver_repository import DashboardDriverRepository
from repository.driver_repository import DriverRepository
from dto.dashboard_driver_input_dto import DashboardDriverInputDto
from dto.dashboard_driver_dto import DashboardDriverDto


class DashboardDriverService:
    def __init__(self, session: Session):
        self._repository = DashboardDriverRepository(session)
        self._driver_repo = DriverRepository(session)

    def create(self, dto: DashboardDriverInputDto) -> DashboardDriverDto:
        driver = self._driver_repo.get_by_id(dto.driver_id)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Piloto não encontrado."
            )

        existing = self._repository.get_by_driver_id(dto.driver_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Configuração de dashboard para este piloto já existe."
            )

        entity = DashboardDriverModel(
            driver_id=dto.driver_id,
            description=dto.description,
            tag_color=dto.tag_color,
            isActive=dto.isActive,
        )
        saved = self._repository.create(entity)
        return DashboardDriverDto.from_entity(saved)

    def get_by_id(self, dashboard_driver_id: str) -> DashboardDriverDto:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Piloto não encontrado."
            )
        return DashboardDriverDto.from_entity(entity)

    def get_all(self, filter_text: Optional[str] = None) -> List[DashboardDriverDto]:
        entities = self._repository.get_all(filter_text=filter_text)
        return [DashboardDriverDto.from_entity(e) for e in entities]

    def update(self, dashboard_driver_id: str, dto: DashboardDriverInputDto) -> DashboardDriverDto:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Piloto não encontrado."
            )

        if dto.driver_id != entity.driver_id:
            driver = self._driver_repo.get_by_id(dto.driver_id)
            if not driver:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Piloto não encontrado."
                )
            existing = self._repository.get_by_driver_id(dto.driver_id)
            if existing and existing.id != entity.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Configuração de dashboard para este piloto já existe."
                )
            entity.driver_id = dto.driver_id

        entity.description = dto.description
        entity.tag_color = dto.tag_color
        entity.isActive = dto.isActive

        updated = self._repository.update(entity)
        return DashboardDriverDto.from_entity(updated)

    def change_status(self, dashboard_driver_id: str, is_active: bool) -> DashboardDriverDto:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Piloto não encontrado"
            )
        entity.isActive = is_active
        updated = self._repository.update(entity)
        return DashboardDriverDto.from_entity(updated)

    def delete(self, dashboard_driver_id: str) -> None:
        entity = self._repository.get_by_id(dashboard_driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Piloto não encontrado"
            )
        self._repository.delete(entity)
