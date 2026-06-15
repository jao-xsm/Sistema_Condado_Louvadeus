from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from src.models.usuario import Usuario
from src.schemas.usuario_schema import CadastroHospedeSchema

def cadastrar_novo_hospede(dados: CadastroHospedeSchema, db: Session):      #RF01

    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    
    #verifica por email se ja temos um usuario cadastrado no sistema
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )
    
    #seguranca da senha usando hashing com bcrypt
    senha_bytes = dados.senha.encode('utf-8')
    sal = bcrypt.gensalt()

    senha_hash = bcrypt.hashpw(senha_bytes, sal).decode('utf-8')

    novo_hospede = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=senha_hash,
        telefone=dados.telefone,
        foto=dados.foto,
        data_nascimento=dados.data_nascimento,
        tipo="hospede"
        )
    
    try:
        db.add(novo_hospede)
        db.commit()
        db.refresh(novo_hospede)
    except Exception as erro:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao salvar no banco de dados: {str(erro)}"
        )
    
    return{
        "mensagem": "Hóspede cadastrado com sucesso!",
        "usuario_id": novo_hospede.id,
        "nome": novo_hospede.nome
    }