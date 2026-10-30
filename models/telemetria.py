class Telemetria:
    def __init__(self, id, piloto_id, carro_numero, session_key,
                 instante, velocidade, distancia):
        self.id = id
        self.piloto_id = piloto_id
        self.carro_numero = carro_numero
        self.session_key = session_key
        self.instante = instante
        self.velocidade = velocidade
        self.distancia = distancia

# representa um registro de telemetria de um piloto em um instante