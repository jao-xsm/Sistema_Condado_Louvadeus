from sqlalchemy import Column, Integer, String, Date
from src.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)#chave primaria implementada pelo PostgreSQL

    #atributos do cadastro de usuario
    nome = Column(String(150), nullable=False)

    email = Column(String(100), unique=True, index=True, nullable=False)

    senha = Column(String(255), nullable=False)

    telefone = Column(String(20), nullable=True)

    foto = Column(String(255), nullable=True)

    data_nascimento = Column(Date, nullable=False)

    tipo = Column(String(20), nullable=False, default="hospede")

    def __repr__(self):
        return f"Usuario(nome='{self.nome}', email='{self.email}', tipo='{self.tipo}')>"