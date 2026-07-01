from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import castas, vinhedos, parcelas, plantios

app = FastAPI(
    title="Winery System ERP",
    description="Production and traceability control system for wineries",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(castas.router)
app.include_router(vinhedos.router)
app.include_router(parcelas.router)
app.include_router(plantios.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Winery System ERP API!"}