from dataclasses import dataclass
from typing import Optional


@dataclass
class HistoricoCorridaDTO:
    piloto: str
    posicao_que_terminou: Optional[int]
    nome_corrida: str                      # organiza os campos que serão usados no json 
    data_corrida: str