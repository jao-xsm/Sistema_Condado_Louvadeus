from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.reserva import Reserva
from src.models.chale import Chale
from src.schemas.reserva_schema import ReservaCreate

def criar_reserva(db: Session, reserva_data: ReservaCreate, hospede_id: int):

    chale = db.query(Chale).filter(Chale.id == reserva_data.chale_id).first()

    if not chale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chalé não encontrado."
        )
    
    reserva_conflitante = db.query(Reserva).filter(
        Reserva.chale_id == reserva_data.chale_id,
        Reserva.status != "CANCELADA",
        Reserva.data_checkin < reserva_data.data_checkout,
        Reserva.data_checkout > reserva_data.data_checkin
    ).first()

    if reserva_conflitante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O chalé já está reservado para este período."
        )
    
    quant_dias = (reserva_data.data_checkout - reserva_data.data_checkin).days
    valor_calculado = quant_dias * chale.val_diaria

    nova_reserva = Reserva(
        hospede_id=hospede_id,
        chale_id=reserva_data.chale_id,
        data_checkin=reserva_data.data_checkin,
        data_checkout=reserva_data.data_checkout,
        valor_total=valor_calculado,
        status="PENDENTE"
    )

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva

def listar_reservas(db: Session, hospede_id: int):
    return db.query(Reserva).filter(Reserva.hospede_id == hospede_id).all()