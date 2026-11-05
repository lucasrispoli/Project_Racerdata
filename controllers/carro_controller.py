from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.carro_service import CarroService

router = APIRouter(prefix="/carros", tags=["Carros"])  # rotas para se usar a API de carros
service = CarroService()


class CarroEntrada(BaseModel):
    numero: int
    piloto_id: str
    marca: str
    categoria: str


@router.post("/")
def criar_carro(dados: CarroEntrada):
    try:
        return service.criar_carro(
            dados.numero, dados.piloto_id, dados.marca, dados.categoria
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/")
def listar_carros():
    return service.listar_carros()


@router.get("/{numero}")
def buscar_carro(numero: int):
    carro = service.buscar_por_numero(numero)
    if carro is None:  # tratamento de erro caso o carro não seja encontrado
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return carro