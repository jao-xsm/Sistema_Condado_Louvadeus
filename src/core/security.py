import jwt
from datetime import datetime, timedelta, timezone
import bcrypt

SECRET_KEY = "chave_super_secreta_cl"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 60

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