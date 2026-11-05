from models.carro import Carro  # ajuste o nome do arquivo se o seu for diferente


class CarroRepository:
    def __init__(self):
        self.carros = {}  # numero do carro -> objeto Carro

    def criar(self, numero, piloto, marca, categoria):
        carro = Carro(numero, piloto, marca, categoria)
        self.carros[numero] = carro
        return carro

    def buscar_por_numero(self, numero):
        return self.carros.get(numero)

    def listar_todos(self):
        return list(self.carros.values())