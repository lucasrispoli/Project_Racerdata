from typing import Optional, List
from sqlalchemy.orm import Session

from entity.session import Session as SessionModel
from entity.driver import Driver as DriverModel
from entity.session_driver import SessionDriver as SessionDriverModel
from repository.session_repository import SessionRepository
from repository.driver_repository import DriverRepository
from repository.session_driver_repository import SessionDriverRepository
from repository.dashboard_driver_repository import DashboardDriverRepository
from dto.dashboard_dto import (
    DashboardFilterDto,
    DashboardOverviewDto,
    DriverPerformanceDto,
    PerformancePointDto,
)
from dto.session_dto import SessionDto
from dto.session_driver_dto import SessionDriverDto

OPENF1_BASE_URL = "https://api.openf1.org/v1"
HTTP_TIMEOUT = 12


class DashboardService:
    def __init__(self, session: Session):
        self._db = session
        self._session_repo = SessionRepository(session)
        self._driver_repo = DriverRepository(session)
        self._session_driver_repo = SessionDriverRepository(session)
        self._dashboard_driver_repo = DashboardDriverRepository(session)

    def get_overview(self, filters: Optional[DashboardFilterDto] = None) -> DashboardOverviewDto:
        filters = filters or DashboardFilterDto()

        all_sessions = self._session_repo.get_all(year=filters.year, session_type=filters.session_type)
        all_drivers = self._driver_repo.get_all()
        active_dash_drivers = self._dashboard_driver_repo.get_all(is_active=True)

        years = sorted(list({s.year for s in all_sessions if s.year}))

        driver_performance: List[DriverPerformanceDto] = []
        for dd in active_dash_drivers:
            participations = self._session_driver_repo.get_by_driver_id(dd.driver_id)
            points: List[PerformancePointDto] = []

            for p in participations:
                if filters.year and p.session.year != filters.year:
                    continue
                if filters.session_type and p.session.session_type != filters.session_type:
                    continue
                if filters.team_name and p.team_name and filters.team_name.lower() not in p.team_name.lower():
                    continue

                points.append(
                    PerformancePointDto(
                        session_name=p.session.session_name or "GP",
                        session_date=(p.session.date_start or "")[:10],
                        car_number=p.car_number,
                        team_name=p.team_name,
                        value=p.car_number,
                    )
                )

            points.sort(key=lambda pt: pt.session_date)

            driver_performance.append(
                DriverPerformanceDto(
                    driver_id=str(dd.driver_id),
                    driver_name=dd.driver.driver_name if dd.driver else "Unknown",
                    tag_color=dd.tag_color or "#E10600",
                    points=points,
                )
            )

        return DashboardOverviewDto(
            total_sessions=len(all_sessions),
            total_drivers=len(all_drivers),
            active_dashboard_drivers=len(active_dash_drivers),
            available_years=years,
            drivers_performance=driver_performance,
        )

    def get_sessions_table(self, filters: Optional[DashboardFilterDto] = None) -> List[SessionDto]:
        filters = filters or DashboardFilterDto()
        entities = self._session_repo.get_all(year=filters.year, session_type=filters.session_type)
        return [SessionDto.model_validate(e) for e in entities]

    def get_session_participants(self, session_id: str) -> List[SessionDriverDto]:
        entities = self._session_driver_repo.get_by_session_id(session_id)
        return [SessionDriverDto.from_entity(e) for e in entities]
