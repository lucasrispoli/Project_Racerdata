from typing import Optional
from pydantic import BaseModel, ConfigDict
from entity.driver import Driver


class DriverInputDto(BaseModel):
    name: str
    description: Optional[str] = ""
    status: bool = True  # Recebe o campo status enviado pelo front (ou active)


class DriverStatusUpdateDto(BaseModel):
    status: bool


class DriverDto(BaseModel):
    id: str
    name: str
    description: str
    status: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, driver: Driver) -> "DriverDto":
        """
        Mapeia a entidade Driver para o DTO que o front-end consome.
        Converte o campo 'active' da entidade para 'status' do DTO.
        """
        return cls(
            id=str(driver.id),
            name=driver.name,
            description=driver.description or "",
            status=bool(driver.active),
        )
