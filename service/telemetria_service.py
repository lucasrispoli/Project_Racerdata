from repositorios_compartilhados import (
    piloto_repository,
    carro_repository,
    telemetria_repository
)
from repositories.corrida_repository import CorridaRepository

VELOCIDADE_MAXIMA = 400   # km/h, acima disso consideramos o valor inválido
MINIMO_REGISTROS = 1      # quantidade mínima de dados válidos para gerar estatística


class TelemetriaService:  # regras de negocio da telemetria
    def __init__(self):
        self.repository = telemetria_repository
        self.piloto_repository = piloto_repository
        self.carro_repository = carro_repository
        self.corrida_repository = CorridaRepository()

    def _eh_numero(self, valor):
        # aceita int ou float (e não aceita True/False)
        if isinstance(valor, bool):
            return False
        return isinstance(valor, (int, float))

    def _piloto_esta_na_sessao(self, piloto, session_key):
        # consulta na OpenF1 quem participou da sessão e compara pelo nome
        participantes = self.corrida_repository.buscar_pilotos_da_corrida(
            session_key
        )

        for p in participantes:
            nome_api = p.get("full_name") or ""
            if nome_api.casefold() == piloto.nome.casefold():
                return True

        return False

    def registrar_telemetria(self, piloto_id, carro_numero, session_key,
                             instante, velocidade, distancia):
        # regra 6: piloto precisa existir no cadastro
        piloto = self.piloto_repository.buscar_por_id(piloto_id)
        if piloto is None:
            raise ValueError("Piloto não cadastrado.")

        # regra 6: carro precisa existir no cadastro
        carro = self.carro_repository.buscar_por_numero(carro_numero)
        if carro is None:
            raise ValueError("Carro não cadastrado.")

        # regra 1: piloto precisa ter participado da sessão informada
        if not self._piloto_esta_na_sessao(piloto, session_key):
            raise ValueError("O piloto não participou da sessão informada.")

        # regra 5: velocidade precisa ser um número válido
        if not self._eh_numero(velocidade):
            raise ValueError("Velocidade inválida.")

        # regra 5 e 4: velocidade negativa não é armazenada
        if velocidade < 0:
            raise ValueError("A velocidade não pode ser negativa.")

        if velocidade > VELOCIDADE_MAXIMA:
            raise ValueError("Velocidade acima do limite aceito.")

        # regra 5: distância precisa ser um número válido
        if not self._eh_numero(distancia):
            raise ValueError("Distância inválida.")

        # regra 10: distância negativa não é armazenada
        if distancia < 0:
            raise ValueError("A distância não pode ser negativa.")

        # o instante da coleta é obrigatório (é usado para achar duplicados)
        if not instante or not str(instante).strip():
            raise ValueError("O instante da coleta é obrigatório.")

        # regra 7: não pode repetir piloto no mesmo instante
        if self.repository.existe_duplicado(piloto_id, instante):
            raise ValueError(
                "Já existe telemetria desse piloto nesse instante."
            )

        return self.repository.salvar(
            piloto_id, carro_numero, session_key,
            instante, velocidade, distancia
        )

    def listar_por_piloto(self, piloto_id):
        piloto = self.piloto_repository.buscar_por_id(piloto_id)
        if piloto is None:
            raise ValueError("Piloto não cadastrado.")

        return self.repository.listar_por_piloto(piloto_id)

    def calcular_estatisticas(self, piloto_id):
        piloto = self.piloto_repository.buscar_por_id(piloto_id)
        if piloto is None:
            raise ValueError("Piloto não cadastrado.")

        registros = self.repository.listar_por_piloto(piloto_id)

        # regra 4: só entram na análise velocidades que não são negativas
        velocidades = []
        for registro in registros:
            if registro.velocidade >= 0:
                velocidades.append(registro.velocidade)

        # regra 9: sem dados válidos suficientes, não gera estatística
        if len(velocidades) < MINIMO_REGISTROS:
            raise ValueError(
                "Não há dados válidos suficientes para gerar estatísticas."
            )

        return {
            "piloto_id": piloto_id,
            "quantidade_registros": len(velocidades),
            "velocidade_media": sum(velocidades) / len(velocidades),
            "velocidade_maxima": max(velocidades)
        }