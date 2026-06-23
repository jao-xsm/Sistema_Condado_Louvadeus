from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.usuario_schema import CadastroHospedeSchema, TokenResponse, LoginRequest, UsuarioUpdate, UsuarioResponse
from src.controllers import usuario_controller
from src.models.usuario import Usuario
from src.core.security import verificar_senha, criar_token_acesso, obter_usuario_atual

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
        "tipo_usuario": usuario.tipo
    }
    token = criar_token_acesso(dados_usuario=dados_token)

    return{
        "access_token": token,
        "token_type": "bearer",
        "tipo_usuario": usuario.tipo
    }

@router.patch("/perfil", response_model=UsuarioResponse)
def editar_perfil(
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    dados_token: dict = Depends(obter_usuario_atual)
):
    usuario_id = int(dados_token["sub"])

    return usuario_controller.atualizar_usuario(
        db=db,
        usuario_id=usuario_id,
        dados_atualizacao=dados
    )

@router.post("/login-swagger", include_in_schema=False)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
    
    dados_token = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "tipo_usuario": usuario.tipo
    }
    token = criar_token_acesso(dados_usuario=dados_token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
