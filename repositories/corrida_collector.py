from repositories.openf1_repository import OpenF1Repository


class CorridaCollector:
    def __init__(self):
        self.api = OpenF1Repository()     #utiliza o openf1 para consultar os dados disponiveis

    def buscar_sessoes(self, parametros=None):
        return self.api.buscar_sessoes(parametros)

    def buscar_corridas(self, ano):
        return self.buscar_sessoes({     #metodo para busca de corridas pelo ano e nome do grande premio
            "year": ano,                  
            "session_name": "Race"
        })

    def buscar_qualificacoes(self, ano):
        return self.buscar_sessoes({
            "year": ano,                     #metdo para busca de qualificações pelo ano e nome do grande premio
            "session_name": "Qualifying"
        })

    def buscar_pilotos_sessao(self, session_key):
        return self.api.buscar_pilotos({
            "session_key": session_key                #metodo para busca de piloto em uma determinada etapa
        })

    def buscar_voltas(self, session_key):
        return self.api.buscar_voltas({                    #metodo para busca de voltas em uma determinada etapa
            "session_key": session_key
        })

    def buscar_resultados_voltas(self, session_key):
        return self.buscar_voltas(session_key)                    

    def buscar_posicoes_sessao(self, session_key):         #metodo para busca de posicoes dos pilotos em uma determinada etapa
        return self.api._buscar_dados(
            "position",
            {"session_key": session_key}
        )

    def buscar_dados_gp(self, meeting_key):              #metodo para busca de dados do grande premio em uma determinada etapa
        return self.api.buscar_reunioes({
            "meeting_key": meeting_key
        })
