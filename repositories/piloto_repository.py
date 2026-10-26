
from models.piloto import Piloto
from uuid import uuid4


class PilotoRepository:
    def __init__(self):
        self.pilotos = {}

    def criar(self, nome, descricao, active=True,
              nacionalidade=None, numero=None):
        piloto_id = str(uuid4())

        piloto = Piloto(
            id=piloto_id,
            nome=nome,
            descricao=descricao,
            active=active,
            nacionalidade=nacionalidade,
            numero=numero
        )

        self.pilotos[piloto_id] = piloto
        return piloto

    def buscar_por_id(self, piloto_id):
        return self.pilotos.get(piloto_id)

    def listar_todos(self):
        return list(self.pilotos.values())

    def atualizar(self, piloto_id, nome, descricao, active):
        piloto = self.buscar_por_id(piloto_id)

        if piloto is None:
            return None

        piloto.nome = nome
        piloto.descricao = descricao
        piloto.active = active

        return piloto

    def excluir(self, piloto_id):
        return self.pilotos.pop(piloto_id, None) is not None

    def alterar_status(self, piloto_id):
        piloto = self.buscar_por_id(piloto_id)

        if piloto is None:
            return None

        piloto.active = not piloto.active
        return piloto
