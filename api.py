from fastapi import FastAPI

from controllers.piloto_controller import router as piloto_router
from controllers.corrida_controller import router as corrida_router
from controllers.carro_controller import router as carro_router
from controllers.telemetria_controller import router as telemetria_router

app = FastAPI(title="RACERDATA")

app.include_router(piloto_router)       # Inclui as rotas do controlador de pilotos
app.include_router(corrida_router)      # Inclui as rotas do controlador de corridas
app.include_router(carro_router)        # Inclui as rotas do controlador de carros
app.include_router(telemetria_router)   # Inclui as rotas do controlador de telemetria