from uuid import uuid4

from models.telemetria import Telemetria


class TelemetriaRepository:
    def __init__(self):
        self.telemetrias = []  # lista para armazenar os objetos de telemetria

    def salvar(self, piloto_id, carro_numero, session_key,
               instante, velocidade, distancia):
        telemetria = Telemetria(
            id=str(uuid4()),
            piloto_id=piloto_id,
            carro_numero=carro_numero,
            session_key=session_key,
            instante=instante,
            velocidade=velocidade,
            distancia=distancia
        )

        self.telemetrias.append(telemetria)
        return telemetria

    def listar_todos(self):
        return list(self.telemetrias)

    def listar_por_piloto(self, piloto_id):
        resultado = []
        for telemetria in self.telemetrias:
            if telemetria.piloto_id == piloto_id:
                resultado.append(telemetria)
        return resultado

    def existe_duplicado(self, piloto_id, instante):
        # true se já existe registro desse piloto nesse mesmo instante
        for telemetria in self.telemetrias:
            if telemetria.piloto_id == piloto_id and telemetria.instante == instante:
                return True
        return False