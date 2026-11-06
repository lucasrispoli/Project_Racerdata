from typing import Optional, List, Dict
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repository.session_driver_repository import SessionDriverRepository
from repository.dashboard_driver_repository import DashboardDriverRepository
from dto.session_driver_dto import SessionDriverDto
from dto.session_driver_line_chart_dto import SessionDriverLineChartDto, LineChartPointDto
from dto.session_driver_results_dto import (
    SessionDriverResultsDto,
    SessionResultDetailDto,
    DriverPositionResultDto,
)


class SessionDriverService:
    def __init__(self, session: Session):
        self._repository = SessionDriverRepository(session)
        self._dash_driver_repo = DashboardDriverRepository(session)

    def get_by_id(self, session_driver_id: str) -> SessionDriverDto:
        entity = self._repository.get_by_id(session_driver_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SessionDriver com id '{session_driver_id}' não encontrado."
            )
        return SessionDriverDto.from_entity(entity)

    def get_all(self, filter_text: Optional[str] = None) -> List[SessionDriverDto]:
        entities = self._repository.get_all(filter_text=filter_text)
        return [SessionDriverDto.from_entity(e) for e in entities]

    def get_drivers_for_line_chart(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverLineChartDto]:

        if date_from and date_to:
            start_date = date.fromisoformat(date_from)
            end_date = date.fromisoformat(date_to)

        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O campo 'De:' não pode ter uma data maior do que o campo 'Até:'."
            )


        # Regra de negocio: apenas pilotos em DashboardDriver com isActive = True
        active_dash_drivers = self._dash_driver_repo.get_active_drivers()
        if not active_dash_drivers:
            return []

        active_driver_map = {d.driver_id: d for d in active_dash_drivers}

        # Regra de negocio: filtrar dados entre date_from e date_to, e por session_type
        session_driver_records = self._repository.get_by_date_range(
            date_from=date_from,
            date_to=date_to,
            session_type=session_type
        )

        grouped_points: Dict[str, List[LineChartPointDto]] = {
            d.driver_id: [] for d in active_dash_drivers}

        for record in session_driver_records:
            if record.driver_id in active_driver_map:
                dash_driver = active_driver_map[record.driver_id]
                driver_name = record.driver.driver_name if record.driver else ""
                date_end_val = record.session.date_end if record.session else None
                # Usa driver_position se preenchido; fallback para car_number
                position_val = record.driver_position if record.driver_position is not None else record.car_number

                point = LineChartPointDto(
                    x=date_end_val,
                    y=position_val,
                    driver_id=str(record.driver_id),
                    driver_name=driver_name,
                    dashboard_driver_id=str(dash_driver.id),
                    dashboard_driver_description=dash_driver.description or "",
                    dashboard_driver_tag_color=dash_driver.tag_color or "#E10600",
                )
                grouped_points[record.driver_id].append(point)

        results: List[SessionDriverLineChartDto] = []
        for dash_driver in active_dash_drivers:
            driver_name = dash_driver.driver.driver_name if dash_driver.driver else ""
            points = grouped_points.get(dash_driver.driver_id, [])
            points.sort(key=lambda pt: pt.x or "")

            results.append(
                SessionDriverLineChartDto(
                    dashboard_driver_id=str(dash_driver.id),
                    driver_id=str(dash_driver.driver_id),
                    driver_name=driver_name,
                    tag_color=dash_driver.tag_color or "#E10600",
                    description=dash_driver.description or "",
                    points_dto=points,
                )
            )

        return results

    def get_all_results(
        self,
        year: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        session_type: Optional[str] = None
    ) -> List[SessionDriverResultsDto]:
        # Regra de negocio: filtrar resultados entre date_from e date_to (e opcionalmente year e session_type)
        records = self._repository.get_all_results(
            year=year,
            date_from=date_from,
            date_to=date_to,
            session_type=session_type
        )

        # Agrupa por year -> session_id
        grouped: Dict[int, Dict[str, SessionResultDetailDto]] = {}

        for record in records:
            if not record.session:
                continue

            sess_year = record.session.year or 0
            sess_id = str(record.session.id)

            if sess_year not in grouped:
                grouped[sess_year] = {}

            if sess_id not in grouped[sess_year]:
                grouped[sess_year][sess_id] = SessionResultDetailDto(
                    session_id=sess_id,
                    date_end=record.session.date_end,
                    session_type=record.session.session_type,
                    circuit_short_name=record.session.circuit_short_name,
                    drivers_positions_dto=[],
                )

            driver_name = record.driver.driver_name if record.driver else ""
            driver_position_dto = DriverPositionResultDto(
                session_driver_id=str(record.id),
                driver_id=str(record.driver_id),
                driver_name=driver_name,
                team_name=record.team_name,
                car_number=record.car_number,
                driver_position=record.driver_position if record.driver_position is not None else record.car_number,
            )
            grouped[sess_year][sess_id].drivers_positions_dto.append(
                driver_position_dto)

        final_list: List[SessionDriverResultsDto] = []
        for yr, sessions_dict in grouped.items():
            final_list.append(
                SessionDriverResultsDto(
                    year=yr,
                    result_dto=list(sessions_dict.values())
                )
            )

        final_list.sort(key=lambda x: x.year or 0, reverse=True)
        return final_list
