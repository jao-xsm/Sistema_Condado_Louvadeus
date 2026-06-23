from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.reserva_schema import ReservaCreate, ReservaResponse, ReservaUpdate
from src.controllers import reserva_controller
from src.core.security import obter_hospede_atual, obter_usuario_atual
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

@router.put("/{reserva_id}")
def editar_reserva(
    reserva_id: int,
    reserva_data: ReservaUpdate,
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(obter_usuario_atual)
):
    if usuario_atual.get("tipo_usuario") != "hospede":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Apenas hospedes podem gerenciar suas reservas."
        )
    
    return reserva_controller.editar_reserva(
        db=db,
        reserva_id=reserva_id,
        reserva_data=reserva_data,
        usuario_id=int(usuario_atual["sub"])
    )

@router.patch("/{reserva_id}/cancelar")
def cancelar_minha_reserva(
    reserva_id: int, 
    db: Session = Depends(get_db), 
    usuario_atual: dict = Depends(obter_usuario_atual)
):
    if usuario_atual.get("tipo_usuario") != "hospede":
        raise HTTPException(status_code=403, detail="Apenas hóspedes podem cancelar reservas.")
        
    return reserva_controller.cancelar_reserva(
        db=db, 
        reserva_id=reserva_id, 
        usuario_id=int(usuario_atual["sub"])
    )