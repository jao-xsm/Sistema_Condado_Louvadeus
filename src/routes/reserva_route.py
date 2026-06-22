from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.reserva_schema import ReservaCreate, ReservaResponse
from src.controllers import reserva_controller
from src.core.security import obter_hospede_atual
from typing import List

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def realizar_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    hospede_logado: dict = Depends(obter_hospede_atual)
):
    hospede_id = hospede_logado.get("id")

    return reserva_controller.criar_reserva(db=db, reserva_data=reserva_data, hospede_id=hospede_id)

@router.get("/", response_model=List[ReservaResponse])
def obter_minhas_reservas(db: Session = Depends(get_db), hospede_logado: dict = Depends(obter_hospede_atual)):
    hospede_id = hospede_logado.get("id")
    return reserva_controller.listar_reservas(db=db, hospede_id=hospede_id)