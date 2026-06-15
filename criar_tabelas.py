from src.database import engine, Base

from src.models.usuario import Usuario

print("A conectar à Neon e a gerar as tabelas o PostgreSQL...")

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso na nuvem!")