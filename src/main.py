from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine, Base
import entity  # Importa todas as entidades (Session, Driver, SessionDriver, DashboardDriver)

from controller.session_controller import router as session_router
from controller.driver_controller import router as driver_router
from controller.session_driver_controller import router as session_driver_router
from controller.dashboard_driver_controller import router as dashboard_driver_router
from controller.dashboard_controller import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not connect or create tables on startup: {e}")
    yield


app = FastAPI(
    title="RACERDATA API",
    description="API de sessões, pilotos e dashboard da Fórmula 1 integrada à OpenF1",
    version="2.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(dashboard_driver_router)
app.include_router(driver_router)
app.include_router(session_router)
app.include_router(session_driver_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "RACERDATA API", "version": "2.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
