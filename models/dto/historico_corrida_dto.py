
from dataclasses import dataclass


@dataclass
class HistoricoCorridaDTO:
    piloto: str
    posicao_que_terminou: int | None
    nome_corrida: str
    data_corrida: str
