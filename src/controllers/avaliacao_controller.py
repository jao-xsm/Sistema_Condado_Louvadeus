from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.avaliacao import Avaliacao
from src.models.usuario import Usuario

def criar_avaliacao(db: Session, hospede_id: int, avaliacao_data):
    nova_avaliacao = Avaliacao(
        hospede_id=hospede_id,
        chale_id=avaliacao_data.chale_id,
        nota=avaliacao_data.nota,
        comentario=avaliacao_data.comentario
    )
    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)
    return nova_avaliacao

# Função para listar as avaliações de um chalé específico
def listar_avaliacoes_por_chale(db: Session, chale_id: int):
    return db.query(Avaliacao).filter(Avaliacao.chale_id == chale_id).all()

# Função que calcula a média para aparecer no seu card (manu)
def calcular_media_chale(db: Session, chale_id: int):
    resultado = db.query(func.avg(Avaliacao.nota)).filter(Avaliacao.chale_id == chale_id).scalar()
    
    return round(resultado, 1) if resultado else 0.0