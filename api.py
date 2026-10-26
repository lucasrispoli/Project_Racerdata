from fastapi import FastAPI

from controllers.piloto_controller import router as piloto_router
from controllers.corrida_controller import router as corrida_router

app = FastAPI(title="RACERDATA")

app.include_router(piloto_router)
app.include_router(corrida_router)
