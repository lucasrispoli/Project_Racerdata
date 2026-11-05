from typing import Optional, List
from sqlalchemy.orm import Session
from entity.session import Session as SessionModel


class SessionRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, session_id: str) -> Optional[SessionModel]:
        return self._db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def get_by_session_key(self, session_key: int) -> Optional[SessionModel]:
        return self._db.query(SessionModel).filter(SessionModel.session_key == session_key).first()

    def get_all(
        self,
        year: Optional[int] = None,
        session_type: Optional[str] = None,
        country_name: Optional[str] = None,
    ) -> List[SessionModel]:
        query = self._db.query(SessionModel)
        if year:
            query = query.filter(SessionModel.year == year)
        if session_type:
            query = query.filter(SessionModel.session_type.ilike(f"%{session_type}%"))
        if country_name:
            query = query.filter(SessionModel.country_name.ilike(f"%{country_name}%"))
        return query.order_by(SessionModel.date_start.asc()).all()

    def create(self, session_entity: SessionModel) -> SessionModel:
        self._db.add(session_entity)
        self._db.commit()
        self._db.refresh(session_entity)
        return session_entity

    def update(self, session_entity: SessionModel) -> SessionModel:
        self._db.commit()
        self._db.refresh(session_entity)
        return session_entity

    def delete(self, session_entity: SessionModel) -> bool:
        self._db.delete(session_entity)
        self._db.commit()
        return True
