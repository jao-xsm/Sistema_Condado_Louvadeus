from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    hospede_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    chale_id = Column(Integer, ForeignKey("chales.id", ondelete="CASCADE"), nullable=False)
    
    nota = Column(Integer, nullable=False) # De 0 a 5
    comentario = Column(String, nullable=True) # Opcional
    
    # Salva a data e hora automaticamente pelo Postgres
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos para facilitar as buscas
    hospede = relationship("Usuario")
    chale = relationship("Chale")