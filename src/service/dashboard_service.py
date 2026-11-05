from typing import Optional, List
import requests
from sqlalchemy.orm import Session

from entity.models import Session as SessionModel, Driver as DriverModel, SessionDriver as SessionDriverModel
from repository.session_repository import SessionRepository
from repository.driver_repository import DriverRepository
from repository.session_driver_repository import SessionDriverRepository
from repository.dashboard_driver_repository import DashboardDriverRepository
from dto.models_dto import (
    CollectDataSummaryDto,
    DashboardFilterDto,
    DashboardOverviewDto,
    DriverPerformanceDto,
    PerformancePointDto,
    SessionDto,
    SessionDriverDto,
)

OPENF1_BASE_URL = "https://api.openf1.org/v1"
HTTP_TIMEOUT = 12


class DashboardService:
    def __init__(self, session: Session):
        self._db = session
        self._session_repo = SessionRepository(session)
        self._driver_repo = DriverRepository(session)
        self._session_driver_repo = SessionDriverRepository(session)
        self._dashboard_driver_repo = DashboardDriverRepository(session)

    def collect_data(self, year: Optional[int] = None) -> CollectDataSummaryDto:
        """
        3 e 4.1 Coleta de dados idempotente da OpenF1:
        - Importa /sessions (Race e Qualifying).
        - Importa /drivers por sessão.
        - Cria / reutiliza Driver.
        - Cria / atualiza SessionDriver com número do carro e equipe.
        """
        summary = CollectDataSummaryDto()

        # 1. Coletar sessões da OpenF1
        params = {}
        if year:
            params["year"] = year

        try:
            resp = requests.get(f"{OPENF1_BASE_URL}/sessions", params=params, timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
            raw_sessions = resp.json()
        except Exception as e:
            summary.errors_count += 1
            return summary

        # Filtra apenas Race e Qualifying
        valid_sessions = [
            s for s in raw_sessions
            if s.get("session_type") in ("Race", "Qualifying") and s.get("session_key") is not None
        ]
        summary.sessions_found = len(valid_sessions)

        # Mapa de cache em memória para evitar queries redundantes no banco
        driver_cache = {d.driver_name: d for d in self._driver_repo.get_all()}

        for s_data in valid_sessions:
            s_key = s_data["session_key"]
            try:
                # 2. Persistir ou atualizar Session
                session_obj = self._session_repo.get_by_session_key(s_key)
                if not session_obj:
                    session_obj = SessionModel(
                        session_key=s_key,
                        meeting_key=s_data.get("meeting_key"),
                        session_name=s_data.get("session_name"),
                        session_type=s_data.get("session_type"),
                        year=s_data.get("year"),
                        country_name=s_data.get("country_name"),
                        location=s_data.get("location"),
                        circuit_short_name=s_data.get("circuit_short_name"),
                        date_start=s_data.get("date_start"),
                        date_end=s_data.get("date_end"),
                        is_cancelled=bool(s_data.get("is_cancelled", False)),
                    )
                    self._session_repo.create(session_obj)
                    summary.sessions_new += 1
                else:
                    session_obj.session_name = s_data.get("session_name")
                    session_obj.session_type = s_data.get("session_type")
                    session_obj.year = s_data.get("year")
                    session_obj.country_name = s_data.get("country_name")
                    session_obj.location = s_data.get("location")
                    session_obj.circuit_short_name = s_data.get("circuit_short_name")
                    session_obj.date_start = s_data.get("date_start")
                    session_obj.date_end = s_data.get("date_end")
                    session_obj.is_cancelled = bool(s_data.get("is_cancelled", False))
                    self._session_repo.update(session_obj)
                    summary.sessions_updated += 1

                # 3. Coletar pilotos dessa sessão
                d_resp = requests.get(
                    f"{OPENF1_BASE_URL}/drivers",
                    params={"session_key": s_key},
                    timeout=HTTP_TIMEOUT
                )
                d_resp.raise_for_status()
                drivers_data = d_resp.json()
                summary.drivers_found += len(drivers_data)

                for d_info in drivers_data:
                    full_name = (d_info.get("full_name") or d_info.get("broadcast_name") or "").strip()
                    if not full_name:
                        continue

                    # Localiza ou cadastra o Driver
                    driver_obj = driver_cache.get(full_name)
                    if not driver_obj:
                        driver_obj = self._driver_repo.get_by_name(full_name)
                        if not driver_obj:
                            driver_obj = self._driver_repo.create(DriverModel(driver_name=full_name))
                            summary.drivers_new += 1
                        driver_cache[full_name] = driver_obj

                    # Cria ou atualiza SessionDriver
                    participation = self._session_driver_repo.get_by_session_and_driver(
                        session_obj.id, driver_obj.id
                    )
                    car_num = d_info.get("driver_number")
                    team = d_info.get("team_name")

                    if not participation:
                        participation = SessionDriverModel(
                            session_id=session_obj.id,
                            driver_id=driver_obj.id,
                            car_number=car_num,
                            team_name=team,
                        )
                        self._session_driver_repo.create(participation)
                        summary.participations_created += 1
                    else:
                        participation.car_number = car_num
                        participation.team_name = team
                        self._session_driver_repo.update(participation)
                        summary.participations_updated += 1

            except Exception as e:
                summary.errors_count += 1
                summary.failed_sessions.append(s_key)
                continue

        return summary

    def get_overview(self, filters: Optional[DashboardFilterDto] = None) -> DashboardOverviewDto:
        """
        4.2 Retorna os dados consolidados do dashboard sem novas requisições à OpenF1
        """
        filters = filters or DashboardFilterDto()

        all_sessions = self._session_repo.get_all(year=filters.year, session_type=filters.session_type)
        all_drivers = self._driver_repo.get_all()
        active_dash_drivers = self._dashboard_driver_repo.get_all(is_active=True)

        years = sorted(list({s.year for s in all_sessions if s.year}))

        # Constrói performance para cada piloto ativo do dashboard
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
                        value=p.car_number,  # Métrica contextual da sessão
                    )
                )

            # Ordena pontos por data
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
