from fastapi import FastAPI

from src.routes.usuario_route import router as usuario_router
from src.routes.chale_route import router as chale_router

app = FastAPI(
    title="API - Condado Louvadeus",
    description="Sistema de gerenciamento de hospedagens da pousada."
)

app.include_router(usuario_router)
app.include_router(chale_router)

#para testar se esta no ar
@app.get("/", tags=["Status"])
def root():
    return {
        "mensagem": "Servidor da pousadaCondado Louvadeus funcionando com sucesso!!",
        "banco_de_dados": "Conectado à Neon"
    }