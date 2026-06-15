from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.usuario_schema import CadastroHospedeSchema
from src.controllers import usuario_controller

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar_hospede(dados: CadastroHospedeSchema, db: Session = Depends(get_db)):
    return usuario_controller.cadastrar_novo_hospede(dados, db)