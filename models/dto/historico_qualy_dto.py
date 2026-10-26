from dataclasses import dataclass


@dataclass
class HistoricoQualyDTO:
    piloto: str
    posicao_que_terminou: int | None
    nome_corrida: str
    data_corrida: str
