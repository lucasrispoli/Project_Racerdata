from dataclasses import dataclass


@dataclass
class HistoricoQualyDTO:
    piloto: str                     # organiza campos que serão usados no json na parte de historico de qualificações
    posicao_que_terminou: int | None
    nome_corrida: str
    data_corrida: str
