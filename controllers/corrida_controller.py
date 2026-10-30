from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.corrida_service import CorridaService  # Recebe os parâmetros enviados pelo cliente e chama o CorridaService.


router = APIRouter(prefix="/analises", tags=["Análises"])  # rotas para se usar a API 
service = CorridaService()


class FiltroAnalise(BaseModel):
    pilotos: list[str]
    data_inicio: date
    data_fim: date


@router.post("/corridas/historico")
def historico_corridas(dados: FiltroAnalise):
    if len(dados.pilotos) < 2:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos dois pilotos para comparar."
        )

    try:
        return service.buscar_historico_corridas(
            dados.pilotos, dados.data_inicio, dados.data_fim
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/corridas/ranking")
def ranking_corridas(dados: FiltroAnalise):
    if len(dados.pilotos) < 2:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos dois pilotos para comparar."
        )

    try:
        return service.gerar_ranking_corridas(
            dados.pilotos, dados.data_inicio, dados.data_fim
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/qualificacoes/historico")
def historico_qualificacoes(dados: FiltroAnalise):
    if len(dados.pilotos) < 2:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos dois pilotos para comparar."
        )

    try:
        return service.buscar_historico_qualificacoes(
            dados.pilotos, dados.data_inicio, dados.data_fim
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/qualificacoes/ranking")
def ranking_qualificacoes(dados: FiltroAnalise):
    if len(dados.pilotos) < 2:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos dois pilotos para comparar."
        )

    try:
        return service.gerar_ranking_qualificacoes(
            dados.pilotos, dados.data_inicio, dados.data_fim
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))