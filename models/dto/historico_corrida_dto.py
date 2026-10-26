
from dataclasses import dataclass


@dataclass
class HistoricoCorridaDTO:
    piloto: str
    posicao_que_terminou: int | None
    nome_corrida: str                      #organisa os campos que serão usados no json na parte de historico de corridas
    data_corrida: str
