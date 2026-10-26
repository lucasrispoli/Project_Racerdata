class Piloto:
    def __init__(
        self,
        id,
        nome,
        descricao,
        active=True,
        nacionalidade=None,
        numero=None
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.active = active
        self.nacionalidade = nacionalidade
        self.numero = numero

    def __repr__(self):
        return f"Piloto(id={self.id}, nome='{self.nome}')"

#representa um piloto e seus atributos