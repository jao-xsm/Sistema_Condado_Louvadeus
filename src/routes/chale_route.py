import os
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.chale_schema import ChaleCreate, ChaleResponse
from src.controllers import chale_controller

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
def cadastrar_chale(chale_data: ChaleCreate, db: Session = Depends(get_db)):
    return chale_controller.criar_chale(db=db, chale_data=chale_data, anfitriao_id=1)

# @router.post("/", response_model=ChaleResponse, status_code=status.HTTP_201_CREATED)
# def cadastrar_chale(chale_data: ChaleCreate, db: Session = Depends(get_db), anfitriao_id: int = Depends(verificar_anfitriao)):
#     return chale_controller.criar_chale(db=db, chale_data=chale_data, anfitriao_id=anfitriao_id)