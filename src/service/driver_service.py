from typing import List, Optional
from sqlalchemy.orm import Session
from entity.driver import Driver
from dto.driver_dto import DriverDto, DriverInputDto
from repository.driver_repository import DriverRepository


class DriverService:
    def __init__(self, session: Session):
        self._repository = DriverRepository(session)

    def create(self, input_dto: DriverInputDto) -> DriverDto:
        # Regra de negócio: O sistema não deve armazenar registros duplicados para o mesmo piloto (já existe um com esse nome)
        existing = self._repository.get_by_name(input_dto.name.strip())
        if existing:
            raise ValueError(f"Driver '{input_dto.name}' already exists.")

        driver = Driver(
            name=input_dto.name.strip(),
            description=input_dto.description.strip() if input_dto.description else "",
            active=input_dto.status,
        )
        saved = self._repository.create(driver)
        return DriverDto.from_entity(saved)

    def get_by_id(self, driver_id: str) -> Optional[DriverDto]:
        driver = self._repository.get_by_id(driver_id)
        if not driver:
            return None
        return DriverDto.from_entity(driver)

    def get_all(self, filter_text: Optional[str] = None) -> List[DriverDto]:
        drivers = self._repository.get_all(filter_text=filter_text)
        return [DriverDto.from_entity(d) for d in drivers]

    def update(self, driver_id: str, input_dto: DriverInputDto) -> Optional[DriverDto]:
        driver = self._repository.get_by_id(driver_id)
        if not driver:
            return None

        # Validação de duplicidade caso esteja alterando o nome
        existing = self._repository.get_by_name(input_dto.name.strip())
        if existing and str(existing.id) != str(driver.id):
            raise ValueError(f"Driver '{input_dto.name}' already exists.")

        driver.name = input_dto.name.strip()
        driver.description = input_dto.description.strip() if input_dto.description else ""
        driver.active = input_dto.status

        updated = self._repository.update(driver)
        return DriverDto.from_entity(updated)

    def change_status(self, driver_id: str, status: bool) -> Optional[DriverDto]:
        driver = self._repository.get_by_id(driver_id)
        if not driver:
            return None

        driver.active = status
        updated = self._repository.update(driver)
        return DriverDto.from_entity(updated)

    def delete(self, driver_id: str) -> bool:
        driver = self._repository.get_by_id(driver_id)
        if not driver:
            return False
        return self._repository.delete(driver)
