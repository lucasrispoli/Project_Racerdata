from typing import Optional, List
from sqlalchemy.orm import Session
from entity.dashboard_driver import DashboardDriver as DashboardDriverModel
from entity.driver import Driver as DriverModel


class DashboardDriverRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, dashboard_driver_id: str) -> Optional[DashboardDriverModel]:
        return (
            self._db.query(DashboardDriverModel)
            .filter(DashboardDriverModel.id == dashboard_driver_id)
            .first()
        )

    def get_by_driver_id(self, driver_id: str) -> Optional[DashboardDriverModel]:
        return (
            self._db.query(DashboardDriverModel)
            .filter(DashboardDriverModel.driver_id == driver_id)
            .first()
        )

    def get_all(self, filter_text: Optional[str] = None) -> List[DashboardDriverModel]:
        query = self._db.query(DashboardDriverModel).join(DashboardDriverModel.driver)
        if filter_text:
            query = query.filter(
                DriverModel.driver_name.ilike(f"%{filter_text}%") |
                DashboardDriverModel.description.ilike(f"%{filter_text}%")
            )
        return query.all()

    def get_active_drivers(self) -> List[DashboardDriverModel]:
        return (
            self._db.query(DashboardDriverModel)
            .filter(DashboardDriverModel.isActive == True)
            .all()
        )

    def create(self, entity: DashboardDriverModel) -> DashboardDriverModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: DashboardDriverModel) -> DashboardDriverModel:
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity: DashboardDriverModel) -> bool:
        self._db.delete(entity)
        self._db.commit()
        return True
