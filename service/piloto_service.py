from repositorios_compartilhados import piloto_repository


class PilotoService:  # cordena as consultas
    def __init__(self):
        # usa o repository compartilhado (o mesmo do TelemetriaService)
        self.repository = piloto_repository

    def criar_piloto(self, nome, descricao, active=True):
        if not nome.strip():
            raise ValueError("O nome do piloto é obrigatório.")

        return self.repository.criar(nome, descricao, active)

    def buscar_por_id(self, piloto_id):
        return self.repository.buscar_por_id(piloto_id)

    def listar_pilotos(self):
        return self.repository.listar_todos()

    def atualizar_piloto(
        self, piloto_id, nome, descricao, active
    ):
        if not nome.strip():
            raise ValueError("O nome do piloto é obrigatório.")

        return self.repository.atualizar(
            piloto_id, nome, descricao, active
        )

    def excluir_piloto(self, piloto_id):
        return self.repository.excluir(piloto_id)

    def alterar_status(self, piloto_id):
        return self.repository.alterar_status(piloto_id)