from fastapi import FastAPI

from src.routes.usuario_route import router as usuario_router

app = FastAPI(
    title="API - Condado Louvadeus",
    description="Sistema de gerenciamento de hospedagens da pousada."
)

app.include_router(usuario_router)

#para testar se esta no ar
@app.get("/", tags=["Status"])
def root():
    return {
        "mensagem": "Servidor da pousadaCondado Louvadeus funcionando com sucesso!!",
        "banco_de_dados": "Conectado à Neon"
    }