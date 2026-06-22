import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "chave_super_secreta_cl"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login-swagger")

def verificar_senha(senha_digitada: str, senha_criptografada_bd: str) -> bool:
    return bcrypt.checkpw(
        senha_digitada.encode('utf-8'),
        senha_criptografada_bd.encode('utf-8')
    )

def criar_token_acesso(dados_usuario: dict) -> str:
    dados_a_criptografar = dados_usuario.copy()

    tempo_validade = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRES_MINUTES)
    dados_a_criptografar.update({"exp": tempo_validade})

    token_jwt = jwt.encode(dados_a_criptografar, SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> dict:
    erro_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acesso inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise erro_autenticacao
    
def obter_hospede_atual(payload: dict = Depends(obter_usuario_atual)) -> dict:
    if payload.get("tipo_usuario") != "hospede":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta operação é exclusiva para perfis de hóspedes."
        )
    
    if "id" not in payload and "sub" in payload:
        payload["id"] = payload["sub"]

    return payload

def obter_anfitriao_atual(payload: dict = Depends(obter_usuario_atual)) -> dict:
    if payload.get("tipo_usuario") != "anfitriao":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta operação é esclusiva para o Anfitrião."
        )
    if "id" not in payload and "sub" in payload:
        payload["id"] = payload["sub"]

    return payload