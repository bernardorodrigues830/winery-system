from fastapi import FastAPI

# Criando a instância principal do sistema com o título correto do seu ERP
app = FastAPI(
    title="Winery System ERP",
    description="Production and traceability control system for wineries",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Winery System ERP API!"}