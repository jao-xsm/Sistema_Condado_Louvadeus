from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Chale(Base):
    __tablename__ = "chales"

    id = Column(Integer, primary_key=True, index=True)

    anfitriao_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)

    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    val_diaria = Column(Float, nullable=False)
    quant_camas = Column(Integer, nullable=False)
    foto_capa = Column(Text, nullable=False)

    ativo = Column(Boolean, nullable=False)#nao iremos deletar do banco, apenas desativar e não mostrar no site

    fotos = relationship("ChaleFoto", back_populates="chale", cascade="all, delete-orphan")

class ChaleFoto(Base):
    __tablename__ = "chale_fotos"

    id = Column(Integer, primary_key=True, index=True)

    chale_id = Column(Integer, ForeignKey("chales.id", ondelete="CASCADE"), nullable=False)

    url = Column(String, nullable=False)

    chale = relationship("Chale", back_populates="fotos")