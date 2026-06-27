import os
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
import jwt
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.chale_schema import ChaleCreate, ChaleResponse, ChaleUpdate
from src.controllers import chale_controller
from src.core.security import obter_anfitriao_atual, obter_usuario_atual

router = APIRouter(prefix="/chales", tags=["Chalés"])

# SECRET_KEY = os.getenv("SECRET_KEY", "chave_ultra_secret")
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

# def verificar_anfitriao(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         tipo_usuario = payload.get("tipo_usuario")
#         anfitriao_id = payload.get("sub")

#         if tipo_usuario =="hospede":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Acesso negado. Apenas anfitriões podem cadastrar chalés."
#             )
        
#         return int(anfitriao_id)
#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token inválido ou expirado. Faça login novamente"
#         )

@router.post("/", response_model=ChaleResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_chale(chale_data: ChaleCreate, db: Session = Depends(get_db), anfitriao: dict = Depends(obter_anfitriao_atual)):
    anfitriao_id = int(anfitriao["sub"])
    return chale_controller.criar_chale(db=db, chale_data=chale_data, anfitriao_id=anfitriao_id)

# @router.post("/", response_model=ChaleResponse, status_code=status.HTTP_201_CREATED)
# def cadastrar_chale(chale_data: ChaleCreate, db: Session = Depends(get_db), anfitriao_id: int = Depends(verificar_anfitriao)):
#     return chale_controller.criar_chale(db=db, chale_data=chale_data, anfitriao_id=anfitriao_id)

@router.get("/", response_model=List[ChaleResponse], status_code=status.HTTP_200_OK)
def listar_chales(db: Session = Depends(get_db)):
    return chale_controller.listar_chales(db=db)

@router.get("/todos", response_model=List[ChaleResponse])
def listar_todos_chales(db: Session = Depends(get_db), anfitriao: dict = Depends(obter_anfitriao_atual)):
    return chale_controller.listar_todos_chales(db=db)

@router.get("/{chale_id}", response_model=ChaleResponse, status_code=status.HTTP_200_OK)
def obter_info_chale(chale_id: int, db: Session = Depends(get_db)):
    return chale_controller.obter_chale_por_id(db=db, chale_id=chale_id)

@router.patch("/{chale_id}", response_model=ChaleResponse)
def editar_chale(chale_id: int, chale_data: ChaleUpdate, db: Session = Depends(get_db), anfitriao: dict = Depends(obter_anfitriao_atual)):
    anfitriao_id = int(anfitriao["id"])
    return chale_controller.atualizar_chale(db=db, chale_id=chale_id, anfitriao_id=anfitriao_id, chale_data=chale_data)

@router.delete("/{chale_id}", status_code=status.HTTP_200_OK)
def apagar_chale(chale_id: int, db: Session = Depends(get_db), anfitriao: dict = Depends(obter_anfitriao_atual)):
    anfitriao_id = int(anfitriao["id"])
    return chale_controller.excluir_chale(db=db, chale_id=chale_id, anfitriao_id=anfitriao_id)

@router.delete("/{chale_id}/fotos/{foto_id}", status_code=status.HTTP_200_OK)
def remover_foto_chale(
    chale_id: int, 
    foto_id: int, 
    db: Session = Depends(get_db), 
    usuario_logado: dict = Depends(obter_usuario_atual)
):

    if usuario_logado.get("tipo_usuario") != "anfitriao":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Apenas anfitriões podem apagar fotos de chalés."
        )
    
    anfitriao_id = int(usuario_logado["sub"])
    
    return chale_controller.deletar_foto_chale(
        db=db, 
        chale_id=chale_id, 
        foto_id=foto_id, 
        anfitriao_id=anfitriao_id
    )