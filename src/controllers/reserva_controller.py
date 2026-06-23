from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from fastapi import HTTPException, status
from src.models.reserva import Reserva
from src.models.chale import Chale
from src.schemas.reserva_schema import ReservaCreate, ReservaUpdate

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

def editar_reserva(db: Session, reserva_id: int, reserva_data: ReservaUpdate, usuario_id: int):

    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada."
        )
    
    if reserva.hospede_id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar essa reserva."
        )
    
    if reserva.status == "CANCELADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível editar uma reserva que já foi cancelada."
        )
    
    if reserva_data.data_checkin >= reserva_data.data_checkout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de check-in não pode ser posterior à data de check-out."
        )
    
    choque= db.query(Reserva).filter(
        Reserva.chale_id == reserva.chale_id,
        Reserva.status != "CANCELADA", 
        Reserva.id != reserva_id,
        Reserva.data_checkin < reserva_data.data_checkout,
        Reserva.data_checkout > reserva_data.data_checkin
    ).first()

    if choque:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O chalé já está reservado para o período escolhido."
        )
    
    reserva.data_checkin = reserva_data.data_checkin
    reserva.data_checkout = reserva_data.data_checkout

    chale = db.query(Chale).filter(Chale.id == reserva.chale_id).first()
    quant_dias = (reserva.data_checkout - reserva.data_checkin).days
    reserva.valor_total = quant_dias * chale.val_diaria

    db.commit()
    db.refresh(reserva)
    return reserva

def cancelar_reserva(db: Session, reserva_id: int, usuario_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada.")
        
    if reserva.hospede_id != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
        
    if reserva.status == "CANCELADA":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A reserva já está cancelada.")

    hoje = datetime.now().date()

    data_limite_cancelamento = reserva.data_checkin - timedelta(days=2)

    if hoje > data_limite_cancelamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O cancelamento só é permitido com pelo menos 48 horas de antecedência do check-in."
        )
    
    reserva.status = "CANCELADA"
    db.commit()
    db.refresh(reserva)

    return {"mensagem": "Reserva cancelada com sucesso", "reserva": reserva}

def listar_reservas(db: Session, hospede_id: int):
    return db.query(Reserva).filter(Reserva.hospede_id == hospede_id).all()