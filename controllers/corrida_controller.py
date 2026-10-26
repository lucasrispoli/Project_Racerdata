
from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.corrida_service import CorridaService


router = APIRouter(prefix="/analises", tags=["Análises"])
service = CorridaService()


class FiltroAnalise(BaseModel):
    pilotos: list[str]
    data_inicio: date
    data_fim: date


def executar_analise(funcao, dados):
    if len(dados.pilotos) < 2:
        raise HTTPException(
            400,
            "Informe pelo menos dois pilotos para comparar."
        )

    try:
        return funcao(
            dados.pilotos,
            dados.data_inicio,
            dados.data_fim
        )
    except ValueError as erro:
        raise HTTPException(400, str(erro))


@router.post("/corridas/historico")
def historico_corridas(dados: FiltroAnalise):
    return executar_analise(
        service.buscar_historico_corridas, dados
    )


@router.post("/corridas/ranking")
def ranking_corridas(dados: FiltroAnalise):
    return executar_analise(
        service.gerar_ranking_corridas, dados
    )


@router.post("/qualificacoes/historico")
def historico_qualificacoes(dados: FiltroAnalise):
    return executar_analise(
        service.buscar_historico_qualificacoes, dados
    )


@router.post("/qualificacoes/ranking")
def ranking_qualificacoes(dados: FiltroAnalise):
    return executar_analise(
        service.gerar_ranking_qualificacoes, dados
    )
