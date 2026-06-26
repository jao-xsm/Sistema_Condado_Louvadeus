from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)

    hospede_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    chale_id = Column(Integer, ForeignKey("chales.id", ondelete="CASCADE"), nullable=False)

    data_checkin = Column(Date, nullable=False)
    data_checkout = Column(Date, nullable=False)

    valor_total = Column(Float, nullable=False)

    status = Column(String, default="Aguardando data do Check-in", nullable=False)

    hospede = relationship("Usuario")
    chale = relationship("Chale")