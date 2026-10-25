from repositories.openf1_repository import OpenF1Repository


class CorridaRepository:
    def __init__(self):
        self.api = OpenF1Repository()

    def buscar_corrida(self, ano, pais):
        parametros = {
            "year": ano,
            "country_name": pais,
            "session_name": "Race"
        }

        sessoes = self.api.buscar_sessoes(parametros)

        if not sessoes:
            return None

        return sessoes[0]

    def buscar_dados_gp(self, meeting_key):
        parametros = {
            "meeting_key": meeting_key
        }

        dados = self.api.buscar_reunioes(parametros)

        if not dados:
            return None

        return dados[0]

    def buscar_pilotos_da_corrida(self, session_key):
        parametros = {
            "session_key": session_key
        }

        return self.api.buscar_pilotos(parametros)

    def buscar_voltas_da_corrida(self, session_key):
        parametros = {
            "session_key": session_key
        }

        return self.api.buscar_voltas(parametros)
