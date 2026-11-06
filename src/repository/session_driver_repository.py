from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from entity.session_driver import SessionDriver as SessionDriverModel
from entity.session import Session as SessionModel


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

    def get_all(self, filter_text: Optional[str] = None) -> List[SessionDriverModel]:
        query = (
            self._db.query(SessionDriverModel)
            .options(joinedload(SessionDriverModel.session), joinedload(SessionDriverModel.driver))
        )
        if filter_text:
            query = query.filter(SessionDriverModel.team_name.ilike(f"%{filter_text}%"))
        return query.all()

    def get_by_date_range(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverModel]:
        query = (
            self._db.query(SessionDriverModel)
            .join(SessionDriverModel.session)
            .options(joinedload(SessionDriverModel.session), joinedload(SessionDriverModel.driver))
        )
        if date_from:
            query = query.filter(SessionModel.date_end >= date_from)
        if date_to:
            query = query.filter(SessionModel.date_end <= date_to)
        if session_type:
            query = query.filter(SessionModel.session_type.ilike(f"%{session_type}%"))
        return query.order_by(SessionModel.date_end.asc()).all()

    def get_all_results(
        self,
        year: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverModel]:
        query = (
            self._db.query(SessionDriverModel)
            .join(SessionDriverModel.session)
            .options(joinedload(SessionDriverModel.session), joinedload(SessionDriverModel.driver))
        )
        if year:
            query = query.filter(SessionModel.year == year)
        if date_from:
            query = query.filter(SessionModel.date_end >= date_from)
        if date_to:
            query = query.filter(SessionModel.date_end <= date_to)
        if session_type:
            query = query.filter(SessionModel.session_type.ilike(f"%{session_type}%"))
        return query.order_by(SessionModel.year.desc(), SessionModel.date_end.asc()).all()

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
