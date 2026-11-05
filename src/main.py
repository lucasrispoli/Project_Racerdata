from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine, Base
import entity.driver  # Registra os modelos SQLAlchemy
from controller.driver_controller import router as driver_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Database connection failed during startup: {e}")
    yield


app = FastAPI(
    title="RACERDATA API",
    description="API de gerenciamento de pilotos e dados de corrida",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(driver_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "RACERDATA API", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
