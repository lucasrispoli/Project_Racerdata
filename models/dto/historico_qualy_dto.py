from dataclasses import dataclass
from typing import Optional


@dataclass
class HistoricoQualyDTO:
    piloto: str                     # organiza campos que serão usados no json na parte de historico de qualificações
    posicao_que_terminou: Optional[int]
    nome_corrida: str
    data_corrida: str