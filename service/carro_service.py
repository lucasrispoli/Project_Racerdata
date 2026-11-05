from repositorios_compartilhados import carro_repository, piloto_repository


class CarroService:  # regras de negocio dos carros
    def __init__(self):
        self.repository = carro_repository
        self.piloto_repository = piloto_repository

    def criar_carro(self, numero, piloto_id, marca, categoria):
        if numero <= 0:
            raise ValueError("O número do carro deve ser maior que zero.")

        if not marca.strip():
            raise ValueError("A marca do carro é obrigatória.")

        # o piloto do carro precisa estar cadastrado
        piloto = self.piloto_repository.buscar_por_id(piloto_id)
        if piloto is None:
            raise ValueError("Piloto não cadastrado.")

        # não pode existir dois carros com o mesmo número
        if self.repository.buscar_por_numero(numero) is not None:
            raise ValueError("Já existe um carro com esse número.")

        return self.repository.criar(numero, piloto_id, marca, categoria)

    def listar_carros(self):
        return self.repository.listar_todos()

    def buscar_por_numero(self, numero):
        return self.repository.buscar_por_numero(numero)