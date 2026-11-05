from typing import Optional

import requests
from sqlalchemy.orm import Session

from entity.session import Session as SessionModel
from entity.driver import Driver as DriverModel
from entity.session_driver import SessionDriver as SessionDriverModel

from repository.session_repository import SessionRepository
from repository.driver_repository import DriverRepository
from repository.session_driver_repository import SessionDriverRepository

from dto.dashboard_dto import CollectDataSummaryDto


OPENF1_BASE_URL = "https://api.openf1.org/v1"
HTTP_TIMEOUT = 12


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

        # Verifica a disponibilidade da API antes da coleta
        self._check_api_availability()

        summary = CollectDataSummaryDto()

        raw_sessions = self._fetch_sessions(year)

        valid_sessions = self._filter_valid_sessions(raw_sessions)
        summary.sessions_found = len(valid_sessions)

        driver_cache = self._load_driver_cache()

        for session_data in valid_sessions:
            session_key = session_data["session_key"]

            try:
                session_obj = self._sync_session(
                    session_data,
                    summary
                )

                drivers_data = self._fetch_session_drivers(
                    session_key
                )

                summary.drivers_found += len(drivers_data)

                self._sync_session_drivers(
                    session_obj,
                    drivers_data,
                    driver_cache,
                    summary
                )

            except Exception:
                summary.errors_count += 1
                summary.failed_sessions.append(session_key)

        return summary

    def _check_api_availability(self) -> None:
        response = requests.get(
            f"{OPENF1_BASE_URL}/sessions",
            params={"limit": 1},
            timeout=HTTP_TIMEOUT
        )

        response.raise_for_status()

    def _fetch_sessions(
        self,
        year: Optional[int] = None
    ) -> list:

        params = {}

        if year:
            params["year"] = year

        response = requests.get(
            f"{OPENF1_BASE_URL}/sessions",
            params=params,
            timeout=HTTP_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    def _filter_valid_sessions(
        self,
        sessions_data: list
    ) -> list:

        return [
            session_data
            for session_data in sessions_data
            if session_data.get("session_type") in (
                "Race",
                "Qualifying"
            )
            and session_data.get("session_key") is not None
        ]

    def _sync_session(
        self,
        session_data: dict,
        summary: CollectDataSummaryDto
    ) -> SessionModel:

        session_key = session_data["session_key"]

        session_obj = self._session_repo.get_by_session_key(
            session_key
        )

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
            circuit_short_name=session_data.get(
                "circuit_short_name"
            ),
            date_start=session_data.get("date_start"),
            date_end=session_data.get("date_end"),
            is_cancelled=bool(
                session_data.get("is_cancelled", False)
            ),
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
        session_obj.circuit_short_name = session_data.get(
            "circuit_short_name"
        )
        session_obj.date_start = session_data.get("date_start")
        session_obj.date_end = session_data.get("date_end")
        session_obj.is_cancelled = bool(
            session_data.get("is_cancelled", False)
        )

    def _fetch_session_drivers(
        self,
        session_key: int
    ) -> list:

        response = requests.get(
            f"{OPENF1_BASE_URL}/drivers",
            params={"session_key": session_key},
            timeout=HTTP_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    def _load_driver_cache(self) -> dict:

        return {
            driver.driver_name: driver
            for driver in self._driver_repo.get_all()
        }

    def _sync_session_drivers(
        self,
        session_obj: SessionModel,
        drivers_data: list,
        driver_cache: dict,
        summary: CollectDataSummaryDto
    ) -> None:

        for driver_data in drivers_data:
            full_name = self._get_driver_name(driver_data)

            if not full_name:
                continue

            driver_obj = self._get_or_create_driver(
                full_name,
                driver_cache,
                summary
            )

            self._sync_participation(
                session_obj,
                driver_obj,
                driver_data,
                summary
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

        driver_obj = self._driver_repo.get_by_name(full_name)

        if not driver_obj:
            driver_obj = self._driver_repo.create(
                DriverModel(driver_name=full_name)
            )
            summary.drivers_new += 1

        driver_cache[full_name] = driver_obj

        return driver_obj

    def _sync_participation(
        self,
        session_obj: SessionModel,
        driver_obj: DriverModel,
        driver_data: dict,
        summary: CollectDataSummaryDto
    ) -> None:

        participation = (
            self._session_driver_repo
            .get_by_session_and_driver(
                session_obj.id,
                driver_obj.id
            )
        )

        car_number = driver_data.get("driver_number")
        team_name = driver_data.get("team_name")

        if participation:
            self._update_participation(
                participation,
                car_number,
                team_name
            )

            self._session_driver_repo.update(participation)
            summary.participations_updated += 1

        else:
            participation = self._create_participation(
                session_obj,
                driver_obj,
                car_number,
                team_name
            )

            self._session_driver_repo.create(participation)
            summary.participations_created += 1

    def _create_participation(
        self,
        session_obj: SessionModel,
        driver_obj: DriverModel,
        car_number: Optional[int],
        team_name: Optional[str]
    ) -> SessionDriverModel:

        return SessionDriverModel(
            session_id=session_obj.id,
            driver_id=driver_obj.id,
            car_number=car_number,
            team_name=team_name,
        )

    def _update_participation(
        self,
        participation: SessionDriverModel,
        car_number: Optional[int],
        team_name: Optional[str]
    ) -> None:

        participation.car_number = car_number
        participation.team_name = team_name