from repositories.openf1_repository import OpenF1Repository


class CorridaCollector:
    def __init__(self):
        self.api = OpenF1Repository()

    def buscar_sessoes(self, parametros=None):
        return self.api.buscar_sessoes(parametros)

    def buscar_corridas(self, ano):
        return self.buscar_sessoes({
            "year": ano,
            "session_name": "Race"
        })

    def buscar_qualificacoes(self, ano):
        return self.buscar_sessoes({
            "year": ano,
            "session_name": "Qualifying"
        })

    def buscar_pilotos_sessao(self, session_key):
        return self.api.buscar_pilotos({
            "session_key": session_key
        })

    def buscar_voltas(self, session_key):
        return self.api.buscar_voltas({
            "session_key": session_key
        })

    def buscar_resultados_voltas(self, session_key):
        return self.buscar_voltas(session_key)

    def buscar_posicoes_sessao(self, session_key):
        return self.api._buscar_dados(
            "position",
            {"session_key": session_key}
        )

    def buscar_dados_gp(self, meeting_key):
        return self.api.buscar_reunioes({
            "meeting_key": meeting_key
        })
