
from dataclasses import dataclass


@dataclass
class RankingCorridaDTO:
    piloto: str                 #define os campos que serão usados no json na parte de ranking de corridas
    qtd_melhor_resultado: int
