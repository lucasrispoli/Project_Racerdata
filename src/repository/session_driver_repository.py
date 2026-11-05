from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from entity.session_driver import SessionDriver as SessionDriverModel


class SessionDriverRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, session_driver_id: str) -> Optional[SessionDriverModel]:
        return (
            self._db.query(SessionDriverModel)
            .options(joinedload(SessionDriverModel.session), joinedload(SessionDriverModel.driver))
            .filter(SessionDriverModel.id == session_driver_id)
            .first()
        )

    def get_by_session_and_driver(self, session_id: str, driver_id: str) -> Optional[SessionDriverModel]:
        return (
            self._db.query(SessionDriverModel)
            .filter(
                SessionDriverModel.session_id == session_id,
                SessionDriverModel.driver_id == driver_id
            )
            .first()
        )

    def get_by_session_id(self, session_id: str) -> List[SessionDriverModel]:
        return (
            self._db.query(SessionDriverModel)
            .options(joinedload(SessionDriverModel.driver))
            .filter(SessionDriverModel.session_id == session_id)
            .all()
        )

    def get_by_driver_id(self, driver_id: str) -> List[SessionDriverModel]:
        return (
            self._db.query(SessionDriverModel)
            .options(joinedload(SessionDriverModel.session))
            .filter(SessionDriverModel.driver_id == driver_id)
            .all()
        )

    def get_all(
        self,
        year: Optional[int] = None,
        driver_id: Optional[str] = None,
        team_name: Optional[str] = None,
    ) -> List[SessionDriverModel]:
        query = (
            self._db.query(SessionDriverModel)
            .options(joinedload(SessionDriverModel.session), joinedload(SessionDriverModel.driver))
        )
        if year:
            query = query.join(SessionDriverModel.session).filter(SessionDriverModel.session.has(year=year))
        if driver_id:
            query = query.filter(SessionDriverModel.driver_id == driver_id)
        if team_name:
            query = query.filter(SessionDriverModel.team_name.ilike(f"%{team_name}%"))
        return query.all()

    def create(self, entity: SessionDriverModel) -> SessionDriverModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: SessionDriverModel) -> SessionDriverModel:
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity: SessionDriverModel) -> bool:
        self._db.delete(entity)
        self._db.commit()
        return True
