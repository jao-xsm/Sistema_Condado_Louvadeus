from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer #sistema q pega o token do cabeçalho de requisição automaticamente
import jwt   #decodifica o token

from src.database import get_db
from src.schemas.usuario_schema import CadastroHospedeSchema, TokenResponse, LoginRequest, UsuarioUpdate, UsuarioResponse
from src.controllers import usuario_controller
from src.models.usuario import Usuario
from src.core.security import verificar_senha, criar_token_acesso, obter_usuario_atual

SECRET_KEY = "chave_super_secreta_cl"
ALGORITHM = "HS256"  #as msm de qnd cria o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login") #"leitor de token" /pega o token do cabeçalho da req auto

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

@router.get("/me")   #rota p buscar os dados
def obterPerfil(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):  #pega o token autom do cabeç
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))  #pega o id do usuario p descobrir qm é
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return{
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "telefone": usuario.telefone,
        "foto": usuario.foto,
        "dataNascimento": str(usuario.data_nascimento),
        "tipo": usuario.tipo
    }