from datetime import date

from repositories.corrida_repository import CorridaRepository

from models.dto.historico_corrida_dto import HistoricoCorridaDTO
from models.dto.ranking_corrida_dto import RankingCorridaDTO
from models.dto.historico_qualy_dto import HistoricoQualyDTO
from models.dto.ranking_qualy_dto import RankingQualyDTO


def pegar_pontos(item):
    # item é uma tupla (nome, pontos); devolve só os pontos
    return item[1]


class CorridaService:
    def __init__(self):
        self.repository = CorridaRepository()

    def _validar_periodo(self, inicio, fim):
        # data inicial não pode ser maior que a data final
        if inicio > fim:
            raise ValueError(
                "A data inicial não pode ser posterior à data final."
            )

        # data final não pode ser no futuro
        if fim > date.today():
            raise ValueError("A data final não pode ser futura.")

    def _obter_posicoes(self, session_key):
        registros = self.repository.buscar_resultados_da_sessao(
            session_key
        )

        # guarda, para cada piloto, a posição mais recente da sessão
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

        # devolve só numero -> posição
        posicoes = {}
        for numero in ultimos:
            posicoes[numero] = ultimos[numero]["position"]

        return posicoes

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

            # nome do piloto -> número do piloto
            por_nome = {}
            for p in pilotos:
                por_nome[p.get("full_name")] = p.get("driver_number")

            # só inclui sessões em que todos os pilotos selecionados participaram
            
            todos_participaram = True
            for nome in nomes:
                if nome not in por_nome:
                    todos_participaram = False

            if not todos_participaram:
                continue

            data_corrida = sessao.get("date_start", "")[:10]
            meeting_key = sessao.get("meeting_key")
            gp = self.repository.buscar_dados_gp(meeting_key)

            if gp:
                nome_gp = gp.get("meeting_name")
            else:
                nome_gp = sessao.get("country_name", "GP desconhecido")

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

        resultado = []
        for nome, posicao, gp, data in dados:
            resultado.append(HistoricoCorridaDTO(nome, posicao, gp, data))

        return resultado

    def buscar_historico_qualificacoes(
        self, pilotos, data_inicio, data_fim
    ):
        dados = self._dados_historico(
            pilotos, data_inicio, data_fim, "Qualifying"
        )

        resultado = []
        for nome, posicao, gp, data in dados:
            resultado.append(HistoricoQualyDTO(nome, posicao, gp, data))

        return resultado

    def _ranking(self, nomes, inicio, fim, tipo):
        self._validar_periodo(inicio, fim)

        sessoes = self.repository.buscar_sessoes_por_periodo(
            inicio, fim, tipo
        )

        # todo mundo começa com 0 pontos
        pontos = {}
        for nome in nomes:
            pontos[nome] = 0

        for sessao in sessoes:
            session_key = sessao.get("session_key")
            if session_key is None:
                continue

            participantes = self.repository.buscar_pilotos_da_corrida(
                session_key
            )
            posicoes = self._obter_posicoes(session_key)

            # nome do piloto -> número do piloto
            por_nome = {}
            for p in participantes:
                por_nome[p.get("full_name")] = p.get("driver_number")

            # nome -> posição, só dos pilotos que estão nesta sessão
            presentes = {}
            for nome in nomes:
                if nome in por_nome:
                    numero = por_nome[nome]
                    if numero in posicoes:
                        presentes[nome] = posicoes[numero]

            # quem terminou à frente do outro ganha 1 ponto
            for nome in presentes:
                for outro in presentes:
                    if nome != outro and presentes[nome] < presentes[outro]:
                        pontos[nome] += 1

        return pontos

    def _ordenar(self, pontos):
        lista = list(pontos.items())
        lista.sort()  # primeiro em ordem alfabética (desempate)
        lista.sort(key=pegar_pontos, reverse=True)  # depois mais pontos primeiro
        return lista

    def gerar_ranking_corridas(self, pilotos, data_inicio, data_fim):
        pontos = self._ranking(pilotos, data_inicio, data_fim, "Race")

        resultado = []
        for nome, pontuacao in self._ordenar(pontos):
            resultado.append(
                RankingCorridaDTO(
                    piloto=nome, qtd_melhor_resultado=pontuacao
                )
            )

        return resultado

    def gerar_ranking_qualificacoes(
        self, pilotos, data_inicio, data_fim
    ):
        pontos = self._ranking(pilotos, data_inicio, data_fim, "Qualifying")

        resultado = []
        for nome, pontuacao in self._ordenar(pontos):
            resultado.append(
                RankingQualyDTO(
                    piloto=nome, qtd_melhor_resultado=pontuacao
                )
            )

        return resultado

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