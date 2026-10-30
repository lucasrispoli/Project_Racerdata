from datetime import date

from repositories.corrida_collector import CorridaCollector


class CorridaRepository:
    def __init__(self):
        self.collector = CorridaCollector()

    def buscar_corrida(self, ano, pais):
        sessoes = self.collector.buscar_corridas(ano)

        for sessao in sessoes:
            if sessao.get("country_name") == pais:
                return sessao

        return None

    def buscar_dados_gp(self, meeting_key):
        dados = self.collector.buscar_dados_gp(meeting_key)
        return dados[0] if dados else None

    def buscar_pilotos_da_corrida(self, session_key):
        return self.collector.buscar_pilotos_sessao(session_key)

    def buscar_voltas_da_corrida(self, session_key):
        return self.collector.buscar_voltas(session_key)

    def buscar_sessoes_por_periodo(
        self, data_inicio, data_fim, tipo_sessao
    ):
        if data_inicio > data_fim:
            raise ValueError(
                "A data inicial não pode ser posterior à data final."
            )

        sessoes_encontradas = []

        for ano in range(data_inicio.year, data_fim.year + 1):
            if tipo_sessao == "Race":
                sessoes = self.collector.buscar_corridas(ano)
            else:
                sessoes = self.collector.buscar_qualificacoes(ano)

            for sessao in sessoes:
                data_texto = sessao.get("date_start")

                if not data_texto:
                    continue

                data_sessao = date.fromisoformat(data_texto[:10])

                if data_inicio <= data_sessao <= data_fim:
                    sessoes_encontradas.append(sessao)

        return sessoes_encontradas

    def buscar_resultados_da_sessao(self, session_key):
        return self.collector.buscar_posicoes_sessao(session_key)
