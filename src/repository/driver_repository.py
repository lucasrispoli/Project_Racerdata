from typing import Optional, List
from sqlalchemy.orm import Session
from entity.driver import Driver as DriverModel


class DriverRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, driver_id: str) -> Optional[DriverModel]:
        return self._db.query(DriverModel).filter(DriverModel.id == driver_id).first()

    def get_by_name(self, driver_name: str) -> Optional[DriverModel]:
        return self._db.query(DriverModel).filter(DriverModel.driver_name == driver_name).first()

    def get_all(self, filter_text: Optional[str] = None) -> List[DriverModel]:
        query = self._db.query(DriverModel)
        if filter_text:
            query = query.filter(DriverModel.driver_name.ilike(f"%{filter_text}%"))
        return query.order_by(DriverModel.driver_name.asc()).all()

    def create(self, driver_entity: DriverModel) -> DriverModel:
        self._db.add(driver_entity)
        self._db.commit()
        self._db.refresh(driver_entity)
        return driver_entity

    def update(self, driver_entity: DriverModel) -> DriverModel:
        self._db.commit()
        self._db.refresh(driver_entity)
        return driver_entity

    def delete(self, driver_entity: DriverModel) -> bool:
        self._db.delete(driver_entity)
        self._db.commit()
        return True
