from typing import List, Optional
from sqlalchemy.orm import Session
from entity.driver import Driver


class DriverRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, driver_id: str) -> Optional[Driver]:
        return self._session.query(Driver).filter(Driver.id == driver_id).first()

    def get_by_name(self, name: str) -> Optional[Driver]:
        return self._session.query(Driver).filter(Driver.name == name).first()

    def get_all(self, filter_text: Optional[str] = None) -> List[Driver]:
        query = self._session.query(Driver)
        if filter_text:
            query = query.filter(Driver.name.ilike(f"%{filter_text}%"))
        return query.all()

    def create(self, driver: Driver) -> Driver:
        self._session.add(driver)
        self._session.commit()
        self._session.refresh(driver)
        return driver

    def update(self, driver: Driver) -> Driver:
        self._session.commit()
        self._session.refresh(driver)
        return driver

    def delete(self, driver: Driver) -> bool:
        self._session.delete(driver)
        self._session.commit()
        return True
