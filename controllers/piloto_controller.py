
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.piloto_service import PilotoService

router = APIRouter(prefix="/pilotos", tags=["Pilotos"])  #rotas para se usar a API de pilotos
service = PilotoService()


class PilotoEntrada(BaseModel):
    nome: str
    descricao: str
    active: bool = True


@router.post("/")
def criar_piloto(dados: PilotoEntrada):
    try:
        return service.criar_piloto(
            dados.nome, dados.descricao, dados.active
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/")
def listar_pilotos():
    return service.listar_pilotos()


@router.get("/{piloto_id}")
def buscar_piloto(piloto_id: str):
    piloto = service.buscar_por_id(piloto_id)
    if piloto is None:                          #tratamento de de erros caso o piloto digitado nao seja encontrado
        raise HTTPException(404, "Piloto não encontrado")
    return piloto


@router.put("/{piloto_id}")
def atualizar_piloto(piloto_id: str, dados: PilotoEntrada):
    piloto = service.atualizar_piloto(
        piloto_id, dados.nome, dados.descricao, dados.active
    )
    if piloto is None:
        raise HTTPException(404, "Piloto não encontrado")   
    return piloto


@router.delete("/{piloto_id}")
def excluir_piloto(piloto_id: str):
    if not service.excluir_piloto(piloto_id):
        raise HTTPException(404, "Piloto não encontrado")
    return {"mensagem": "Piloto excluído com sucesso"}


@router.patch("/{piloto_id}/status")
def alterar_status(piloto_id: str):
    piloto = service.alterar_status(piloto_id)
    if piloto is None:
        raise HTTPException(404, "Piloto não encontrado")
    return piloto
