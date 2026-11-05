import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.telemetria_service import TelemetriaService

router = APIRouter(prefix="/telemetria", tags=["Telemetria"])  # rotas para se usar a API de telemetria
service = TelemetriaService()

class TelemetriaEntrada(BaseModel):
    piloto_id: str
    carro_numero: int
    session_key: int
    instante: str
    velocidade: float
    distancia: float

@router.post("/")
def registrar_telemetria(dados: TelemetriaEntrada):
    try:
        return service.registrar_telemetria(
            dados.piloto_id,
            dados.carro_numero,
            dados.session_key,
            dados.instante,
            dados.velocidade,
            dados.distancia
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except requests.RequestException:
        # erro ao consultar a OpenF1 (timeout, sem internet etc.)
        raise HTTPException(
            status_code=502,
            
            detail="Não foi possível consultar a OpenF1 agora."
        )

@router.get("/piloto/{piloto_id}")
def listar_telemetria_do_piloto(piloto_id: str):
    try:
        return service.listar_por_piloto(piloto_id)
    except ValueError as erro:

        raise HTTPException(status_code=400, detail=str(erro))

@router.get("/piloto/{piloto_id}/estatisticas")
def estatisticas_do_piloto(piloto_id: str):
    try:
       
       return service.calcular_estatisticas(piloto_id)
    except ValueError as erro:

        raise HTTPException(status_code=400, detail=str(erro))