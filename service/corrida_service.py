
from datetime import date

from repositories.corrida_repository import CorridaRepository

from models.dto.historico_corrida_dto import HistoricoCorridaDTO
from models.dto.ranking_corrida_dto import RankingCorridaDTO
from models.dto.historico_qualy_dto import HistoricoQualyDTO
from models.dto.ranking_qualy_dto import RankingQualyDTO


class CorridaService:     #regras de negocio 
    def __init__(self):
        self.repository = CorridaRepository()

    def _validar_periodo(self, inicio, fim):
        if inicio > fim:
            raise ValueError(            
                   #valida se a data inicial é maior que a data final, caso seja, retorna o erro 400 com a mensagem
                "A data inicial não pode ser posterior à data final."
            )

        if fim > date.today():
            raise ValueError("A data final não pode ser futura.")   
        #valida se a data final é maior que a data atual, caso seja, retorna o erro 400 com a mensagem

    def _obter_posicoes(self, session_key):
        registros = self.repository.buscar_resultados_da_sessao(
            session_key
        )

        ultimos = {}

        for registro in registros:
            numero = registro.get("driver_number")
            posicao = registro.get("position")
            instante = registro.get("date", "")

            if numero is None or posicao is None:
                continue

            anterior = ultimos.get(numero)

            if anterior is None or instante > anterior["date"]:
                ultimos[numero] = {
                    "date": instante,
                    "position": posicao
                }

        return {
            numero: dados["position"]
            for numero, dados in ultimos.items()
        }

    def _dados_historico(self, nomes, inicio, fim, tipo):
        self._validar_periodo(inicio, fim)

        sessoes = self.repository.buscar_sessoes_por_periodo(
            inicio, fim, tipo
        )
        historico = []

        for sessao in sessoes:
            session_key = sessao.get("session_key")
            if session_key is None:
                continue

            pilotos = self.repository.buscar_pilotos_da_corrida(
                session_key
            )
            posicoes = self._obter_posicoes(session_key)

            por_nome = {
                p.get("full_name"): p.get("driver_number")
                for p in pilotos
            }

            # Só inclui sessões em que todos os pilotos selecionados
            # participaram.
            if not all(nome in por_nome for nome in nomes):
                continue

            data_corrida = sessao.get("date_start", "")[:10]
            meeting_key = sessao.get("meeting_key")
            gp = self.repository.buscar_dados_gp(meeting_key)
            nome_gp = (
                gp.get("meeting_name")
                if gp else sessao.get("country_name", "GP desconhecido")
            )

            for nome in nomes:
                numero = por_nome[nome]
                posicao = posicoes.get(numero)

                historico.append(
                    (nome, posicao, nome_gp, data_corrida)
                )

        return historico

    def buscar_historico_corridas(self, pilotos, data_inicio, data_fim):
        dados = self._dados_historico(
            pilotos, data_inicio, data_fim, "Race"
        )

        return [
            HistoricoCorridaDTO(nome, posicao, gp, data)
            for nome, posicao, gp, data in dados
        ]

    def buscar_historico_qualificacoes(
        self, pilotos, data_inicio, data_fim
    ):
        dados = self._dados_historico(
            pilotos, data_inicio, data_fim, "Qualifying"
        )

        return [
            HistoricoQualyDTO(nome, posicao, gp, data)
            for nome, posicao, gp, data in dados
        ]

    def _ranking(self, nomes, inicio, fim, tipo, dto):
        self._validar_periodo(inicio, fim)

        sessoes = self.repository.buscar_sessoes_por_periodo(
            inicio, fim, tipo
        )
        pontos = {nome: 0 for nome in nomes}

        for sessao in sessoes:
            session_key = sessao.get("session_key")
            if session_key is None:
                continue

            participantes = self.repository.buscar_pilotos_da_corrida(
                session_key
            )
            posicoes = self._obter_posicoes(session_key)

            por_nome = {
                p.get("full_name"): p.get("driver_number")
                for p in participantes
            }

            presentes = {
                nome: posicoes[por_nome[nome]]
                for nome in nomes
                if nome in por_nome and por_nome[nome] in posicoes
            }

            for nome in presentes:
                for outro in presentes:
                    if nome != outro and presentes[nome] < presentes[outro]:
                        pontos[nome] += 1

        ordenados = sorted(
            pontos.items(),
            key=lambda item: (-item[1], item[0])
        )

        return [
            dto(piloto=nome, qtd_melhor_resultado=pontuacao)
            for nome, pontuacao in ordenados
        ]

    def gerar_ranking_corridas(self, pilotos, data_inicio, data_fim):
        return self._ranking(
            pilotos, data_inicio, data_fim,
            "Race", RankingCorridaDTO
        )

    def gerar_ranking_qualificacoes(
        self, pilotos, data_inicio, data_fim
    ):
        return self._ranking(
            pilotos, data_inicio, data_fim,
            "Qualifying", RankingQualyDTO
        )

    # Mantém a consulta de GP que você já usava no main.py.
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
