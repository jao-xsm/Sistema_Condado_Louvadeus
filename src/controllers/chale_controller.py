from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.usuario import Usuario
from src.models.chale import Chale
from src.schemas.chale_schema import ChaleCreate

# def criar_chale(db: Session, chale_data: ChaleCreate):#funcao temporaria sem o jwt do anfitriao logado
#     try:

#         usuario = db.query(Usuario).filter(Usuario.id == chale_data.anfitriao_id).first()
#         if not usuario:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="O anfitrião informado não existe no sistema."
#             )
        
#         if usuario.tipo != "anfitriao":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Apenas anfitriões podem criar novos chalés"
#             )
#         novo_chale = Chale(**chale_data.model_dump())

#         db.add(novo_chale)
#         db.commit()

#         db.refresh(novo_chale)

#         return novo_chale
#     except HTTPException as erro_fastapi:
#         raise erro_fastapi
#     except Exception as erro:
#         db.rollback()

#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro interno ao cadastrar o chalé: {str(erro)}"
#         )
    
#funcao oficial comentada
def criar_chale(db: Session, chale_data: ChaleCreate, anfitriao_id: int):
    try:
        novo_chale = Chale(**chale_data.model_dump(), anfitriao_id=anfitriao_id)
        
        db.add(novo_chale)
        db.commit()
        db.refresh(novo_chale)
        return novo_chale

    except Exception as erro:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao cadastrar o chalé: {str(erro)}"
        )