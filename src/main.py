from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importando o modulo de CORS

from src.routes.usuario_route import router as usuario_router
from src.routes.chale_route import router as chale_router

app = FastAPI(
    title="API - Condado Louvadeus",
    description="Sistema de gerenciamento de hospedagens da pousada."
)

app.add_middleware( # configura o servidor para aceitar requisições do frontend
    CORSMiddleware, 
    allow_origins=["*"], # aceita requisições de qualquer endereço (depois mudar p o endereço só do site msm)
    allow_methods=["*"], # aceita qualquer método (GET, POST, etc.)
    allow_headers=["*"], # aceita qualquer cabeçalho
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