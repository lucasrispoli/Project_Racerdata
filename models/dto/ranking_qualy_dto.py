from dataclasses import dataclass


@dataclass
class RankingQualyDTO:
    piloto: str
    qtd_melhor_resultado: int
