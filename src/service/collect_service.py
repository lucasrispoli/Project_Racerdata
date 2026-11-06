import time
from typing import Optional, Dict, Any, List
import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from entity.session import Session as SessionModel
from entity.driver import Driver as DriverModel
from entity.session_driver import SessionDriver as SessionDriverModel

from repository.session_repository import SessionRepository
from repository.driver_repository import DriverRepository
from repository.session_driver_repository import SessionDriverRepository

from dto.dashboard_dto import CollectDataSummaryDto


OPENF1_BASE_URL = "https://api.openf1.org/v1"
HTTP_TIMEOUT = 15
DEFAULT_HEADERS = {
    "User-Agent": "RacerData-App/2.1 (Formula1-Analysis-Tool)",
    "Accept": "application/json",
}


def _request_with_retry(
    url: str,
    params: Optional[dict] = None,
    max_retries: int = 4,
    backoff_factor: float = 1.5
) -> requests.Response:
    """
    Executa requisição HTTP com headers apropriados e tratamento de Rate Limit (HTTP 429)
    com backoff exponencial.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                params=params,
                headers=DEFAULT_HEADERS,
                timeout=HTTP_TIMEOUT
            )

            # Se recebeu 429 Too Many Requests, aguarda respeitando retry-after ou backoff
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                sleep_time = float(retry_after) if retry_after else (backoff_factor * (2 ** attempt))
                time.sleep(sleep_time)
                continue

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(backoff_factor * (attempt + 1))

    raise requests.exceptions.HTTPError(f"Falha na requisição para {url} após retentativas.")


class DataCollectionService:

    def __init__(self, session: Session):
        self._db = session
        self._session_repo = SessionRepository(session)
        self._driver_repo = DriverRepository(session)
        self._session_driver_repo = SessionDriverRepository(session)

    def collect_data(
        self,
        year: Optional[int] = None
    ) -> CollectDataSummaryDto:
        summary = CollectDataSummaryDto()

        # 1. Busca sessões da OpenF1
        try:
            raw_sessions = self._fetch_sessions(year)
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS if "429" in str(e) else status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenF1 API Rate Limit ou indisponibilidade: {str(e)}"
            )

        valid_sessions = self._filter_valid_sessions(raw_sessions)
        summary.sessions_found = len(valid_sessions)

        # 2. Carrega cache inicial de pilotos por nome
        driver_cache = self._load_driver_cache()

        # 3. Itera e sincroniza cada sessão com espaçamento entre requisições
        for session_data in valid_sessions:
            session_key = session_data.get("session_key")
            if not session_key:
                continue

            try:
                # Salva ou atualiza Session
                session_obj = self._sync_session(session_data, summary)

                # Busca dados de drivers da sessão
                drivers_data = self._fetch_session_drivers(session_key)
                summary.drivers_found += len(drivers_data)

                # Busca dados de session_result da sessão
                results_data = self._fetch_session_results(session_key)

                # Sincroniza SessionDriver cruzando drivers e session_result
                self._sync_session_drivers(
                    session_obj=session_obj,
                    drivers_data=drivers_data,
                    results_data=results_data,
                    driver_cache=driver_cache,
                    summary=summary
                )

            except Exception:
                summary.errors_count += 1
                summary.failed_sessions.append(session_key)

        return summary

    def _fetch_sessions(
        self,
        year: Optional[int] = None
    ) -> list:
        params = {}
        if year:
            params["year"] = year

        response = _request_with_retry(
            f"{OPENF1_BASE_URL}/sessions",
            params=params
        )
        return response.json()

    def _filter_valid_sessions(
        self,
        sessions_data: list
    ) -> list:
        return [
            session_data
            for session_data in sessions_data
            if session_data.get("session_type") in ("Race")
            and session_data.get("session_key") is not None
        ]

    def _sync_session(
        self,
        session_data: dict,
        summary: CollectDataSummaryDto
    ) -> SessionModel:
        session_key = session_data["session_key"]
        session_obj = self._session_repo.get_by_session_key(session_key)

        if session_obj:
            self._update_session(session_obj, session_data)
            self._session_repo.update(session_obj)
            summary.sessions_updated += 1
        else:
            session_obj = self._create_session(session_data)
            self._session_repo.create(session_obj)
            summary.sessions_new += 1

        return session_obj

    def _create_session(
        self,
        session_data: dict
    ) -> SessionModel:
        return SessionModel(
            session_key=session_data["session_key"],
            meeting_key=session_data.get("meeting_key"),
            session_name=session_data.get("session_name"),
            session_type=session_data.get("session_type"),
            year=session_data.get("year"),
            country_name=session_data.get("country_name"),
            location=session_data.get("location"),
            circuit_short_name=session_data.get("circuit_short_name"),
            date_start=session_data.get("date_start"),
            date_end=session_data.get("date_end"),
            is_cancelled=bool(session_data.get("is_cancelled", False)),
        )

    def _update_session(
        self,
        session_obj: SessionModel,
        session_data: dict
    ) -> None:
        session_obj.session_name = session_data.get("session_name")
        session_obj.session_type = session_data.get("session_type")
        session_obj.year = session_data.get("year")
        session_obj.country_name = session_data.get("country_name")
        session_obj.location = session_data.get("location")
        session_obj.circuit_short_name = session_data.get("circuit_short_name")
        session_obj.date_start = session_data.get("date_start")
        session_obj.date_end = session_data.get("date_end")
        session_obj.is_cancelled = bool(session_data.get("is_cancelled", False))

    def _fetch_session_drivers(
        self,
        session_key: int
    ) -> list:
        response = _request_with_retry(
            f"{OPENF1_BASE_URL}/drivers",
            params={"session_key": session_key}
        )
        return response.json()

    def _fetch_session_results(
        self,
        session_key: int
    ) -> list:
        try:
            response = _request_with_retry(
                f"{OPENF1_BASE_URL}/session_result",
                params={"session_key": session_key},
                max_retries=2
            )
            return response.json()
        except Exception:
            return []

    def _load_driver_cache(self) -> dict:
        return {
            driver.driver_name: driver
            for driver in self._driver_repo.get_all()
        }

    def _sync_session_drivers(
        self,
        session_obj: SessionModel,
        drivers_data: list,
        results_data: list,
        driver_cache: dict,
        summary: CollectDataSummaryDto
    ) -> None:
        # Mapa de resultados indexado pelo car/driver_number:
        # {driver_number: position}
        positions_by_car_number: Dict[int, int] = {}
        for result in results_data:
            num = result.get("driver_number")
            pos = result.get("position")
            if num is not None and pos is not None:
                positions_by_car_number[num] = pos

        for driver_data in drivers_data:
            full_name = self._get_driver_name(driver_data)
            if not full_name:
                continue

            driver_obj = self._get_or_create_driver(
                full_name,
                driver_cache,
                summary
            )

            car_number = driver_data.get("driver_number")
            team_name = driver_data.get("team_name")
            driver_position = positions_by_car_number.get(car_number) if car_number is not None else None

            self._sync_participation(
                session_obj=session_obj,
                driver_obj=driver_obj,
                car_number=car_number,
                team_name=team_name,
                driver_position=driver_position,
                summary=summary
            )

    def _get_driver_name(
        self,
        driver_data: dict
    ) -> str:
        return (
            driver_data.get("full_name")
            or driver_data.get("broadcast_name")
            or ""
        ).strip()

    def _get_or_create_driver(
        self,
        full_name: str,
        driver_cache: dict,
        summary: CollectDataSummaryDto
    ) -> DriverModel:
        driver_obj = driver_cache.get(full_name)
        if driver_obj:
            return driver_obj

        driver_obj = self._driver_repo.get_by_name(full_name.upper())
        if not driver_obj:
            driver_obj = self._driver_repo.create(
                DriverModel(driver_name=full_name.upper())
            )
            summary.drivers_new += 1

        driver_cache[full_name] = driver_obj
        return driver_obj

    def _sync_participation(
        self,
        session_obj: SessionModel,
        driver_obj: DriverModel,
        car_number: Optional[int],
        team_name: Optional[str],
        driver_position: Optional[int],
        summary: CollectDataSummaryDto
    ) -> None:
        participation = self._session_driver_repo.get_by_session_and_driver(
            session_obj.id,
            driver_obj.id
        )

        if participation:
            self._update_participation(
                participation=participation,
                car_number=car_number,
                team_name=team_name,
                driver_position=driver_position
            )
            self._session_driver_repo.update(participation)
            summary.participations_updated += 1
        else:
            participation = self._create_participation(
                session_obj=session_obj,
                driver_obj=driver_obj,
                car_number=car_number,
                team_name=team_name,
                driver_position=driver_position
            )
            self._session_driver_repo.create(participation)
            summary.participations_created += 1

    def _create_participation(
        self,
        session_obj: SessionModel,
        driver_obj: DriverModel,
        car_number: Optional[int],
        team_name: Optional[str],
        driver_position: Optional[int]
    ) -> SessionDriverModel:
        return SessionDriverModel(
            session_id=session_obj.id,
            driver_id=driver_obj.id,
            car_number=car_number,
            team_name=team_name,
            driver_position=driver_position
        )

    def _update_participation(
        self,
        participation: SessionDriverModel,
        car_number: Optional[int],
        team_name: Optional[str],
        driver_position: Optional[int]
    ) -> None:
        participation.car_number = car_number
        participation.team_name = team_name
        if driver_position is not None:
            participation.driver_position = driver_position
