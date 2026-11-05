from typing import Optional
from pydantic import BaseModel, ConfigDict


class SessionCreateDto(BaseModel):
    session_key: int
    meeting_key: Optional[int] = None
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: bool = False


class SessionUpdateDto(BaseModel):
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: Optional[bool] = None


class SessionDto(BaseModel):
    id: str
    session_key: int
    meeting_key: Optional[int] = None
    session_name: Optional[str] = None
    session_type: Optional[str] = None
    year: Optional[int] = None
    country_name: Optional[str] = None
    location: Optional[str] = None
    circuit_short_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    is_cancelled: bool = False

    model_config = ConfigDict(from_attributes=True)
