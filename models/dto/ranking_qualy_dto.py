from dataclasses import dataclass


@dataclass
class RankingQualyDTO:              #define os campos que serão usados no json na parte de ranking de qualificações
    piloto: str
    qtd_melhor_resultado: int
