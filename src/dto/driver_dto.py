from pydantic import BaseModel, ConfigDict


class DriverCreateDto(BaseModel):
    driver_name: str


class DriverUpdateDto(BaseModel):
    driver_name: str


class DriverDto(BaseModel):
    id: str
    driver_name: str

    model_config = ConfigDict(from_attributes=True)
