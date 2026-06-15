from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.usuario_schema import CadastroHospedeSchema, TokenResponse, LoginRequest
from src.controllers import usuario_controller
from src.models.usuario import Usuario
from src.core.security import verificar_senha, criar_token_acesso

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_hospede(dados: CadastroHospedeSchema, db: Session = Depends(get_db)):
    return usuario_controller.cadastrar_novo_hospede(dados, db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == payload.email).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
    
    if not verificar_senha(payload.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
    
    dados_token = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "tipo": usuario.tipo
    }
    token = criar_token_acesso(dados_usuario=dados_token)

    return{
        "access_token": token,
        "token_type": "bearer",
        "tipo_usuario": usuario.tipo
    }
