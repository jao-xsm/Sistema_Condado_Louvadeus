from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.avaliacao_schema import AvaliacaoCreate, AvaliacaoResponse
from src.controllers import avaliacao_controller
from src.core.security import obter_usuario_atual 

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def avaliar_chale(
    avaliacao_data: AvaliacaoCreate, 
    db: Session = Depends(get_db), 
    usuario_logado: dict = Depends(obter_usuario_atual)
):
    
    if usuario_logado["tipo_usuario"] != "hospede":
        raise HTTPException(status_code=403, detail="Apenas hóspedes podem avaliar chalés.")
    
    return avaliacao_controller.criar_avaliacao(
        db=db, 
        hospede_id=int(usuario_logado["sub"]), 
        avaliacao_data=avaliacao_data
    )

#Retorna a média de um chalé (Para vc colocar no Card)
@router.get("/chale/{chale_id}/media")
def obter_media_chale(chale_id: int, db: Session = Depends(get_db)):
    media = avaliacao_controller.calcular_media_chale(db=db, chale_id=chale_id)
    return {"chale_id": chale_id, "media": media}

#Retorna a lista de comentários para a página do Chalé
@router.get("/chale/{chale_id}/lista")
def listar_comentarios(chale_id: int, db: Session = Depends(get_db)):
    avaliacoes = avaliacao_controller.listar_avaliacoes_por_chale(db=db, chale_id=chale_id)
    
    
    lista_resposta = []
    for aval in avaliacoes:
        lista_resposta.append({
            "id": aval.id,
            "nome_hospede": aval.hospede.nome, 
            "nota": aval.nota,
            "comentario": aval.comentario,
            "data_criacao": aval.data_criacao
        })
    return lista_resposta