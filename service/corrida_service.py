
from repositories.corrida_repository import CorridaRepository


class CorridaService:
    def __init__(self):
        self.repository = CorridaRepository()

    def buscar_dados_corrida(self, ano, pais):
        corrida = self.repository.buscar_corrida(ano, pais)

        if corrida is None:
            return None

        session_key = corrida["session_key"]
        meeting_key = corrida["meeting_key"]

        gp = self.repository.buscar_dados_gp(meeting_key)
        pilotos = self.repository.buscar_pilotos_da_corrida(
            session_key
        )
        voltas = self.repository.buscar_voltas_da_corrida(
            session_key
        )

        return {
            "corrida": corrida,
            "gp": gp,
            "pilotos": pilotos,
            "voltas": voltas
        }
