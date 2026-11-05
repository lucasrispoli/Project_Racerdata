from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from entity.models import DashboardDriver as DashboardDriverModel


class DashboardDriverRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, dashboard_driver_id: str) -> Optional[DashboardDriverModel]:
        return (
            self._db.query(DashboardDriverModel)
            .options(joinedload(DashboardDriverModel.driver))
            .filter(DashboardDriverModel.id == dashboard_driver_id)
            .first()
        )

    def get_by_driver_id(self, driver_id: str) -> Optional[DashboardDriverModel]:
        return (
            self._db.query(DashboardDriverModel)
            .options(joinedload(DashboardDriverModel.driver))
            .filter(DashboardDriverModel.driver_id == driver_id)
            .first()
        )

    def get_all(
        self,
        is_active: Optional[bool] = None,
        filter_text: Optional[str] = None
    ) -> List[DashboardDriverModel]:
        query = (
            self._db.query(DashboardDriverModel)
            .options(joinedload(DashboardDriverModel.driver))
        )
        if is_active is not None:
            query = query.filter(DashboardDriverModel.isActive == is_active)
        if filter_text:
            query = query.join(DashboardDriverModel.driver).filter(
                DashboardDriverModel.driver.has(
                    DashboardDriverModel.driver.property.mapper.class_.driver_name.ilike(f"%{filter_text}%")
                )
            )
        return query.all()

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
