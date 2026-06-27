from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from src.models.usuario import Usuario
from src.models.chale import Chale, ChaleFoto
from src.models.reserva import Reserva
from src.schemas.chale_schema import ChaleCreate

# def criar_chale(db: Session, chale_data: ChaleCreate):#funcao temporaria sem o jwt do anfitriao logado
#     try:

#         usuario = db.query(Usuario).filter(Usuario.id == chale_data.anfitriao_id).first()
#         if not usuario:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="O anfitrião informado não existe no sistema."
#             )
        
#         if usuario.tipo != "anfitriao":
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Apenas anfitriões podem criar novos chalés"
#             )
#         novo_chale = Chale(**chale_data.model_dump())

#         db.add(novo_chale)
#         db.commit()

#         db.refresh(novo_chale)

#         return novo_chale
#     except HTTPException as erro_fastapi:
#         raise erro_fastapi
#     except Exception as erro:
#         db.rollback()

#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro interno ao cadastrar o chalé: {str(erro)}"
#         )
    
#funcao oficial comentada
def criar_chale(db: Session, chale_data: ChaleCreate, anfitriao_id: int):
    try:
        novo_chale = Chale(
            anfitriao_id=anfitriao_id,
            nome=chale_data.nome,
            descricao=chale_data.descricao,
            val_diaria=chale_data.val_diaria,
            quant_camas=chale_data.quant_camas,
            foto_capa=chale_data.foto_capa,
            ativo=True
        )
        
        db.add(novo_chale)
        db.flush()

        for url_foto in chale_data.galeria_fotos:
            nova_foto = ChaleFoto(chale_id=novo_chale.id, url=url_foto)
            db.add(nova_foto)
    
        db.commit()
        db.refresh(novo_chale)
        return novo_chale

    except Exception as erro:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao cadastrar o chalé: {str(erro)}"
        )
    
def atualizar_chale(db, chale_id: int, anfitriao_id: int, chale_data):
    chale = db.query(Chale).filter(Chale.id == chale_id, Chale.anfitriao_id == anfitriao_id).first()
    
    if not chale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chalé não encontrado ou não pertence a este anfitrião."
        )
    
    dados_atualizacao = chale_data.model_dump(exclude_unset=True)
    fotos_novas = dados_atualizacao.pop("fotos", None)
    for chave, valor in dados_atualizacao.items():
        setattr(chale, chave, valor)

    if fotos_novas is not None:
        for url in fotos_novas:
             nova_foto = ChaleFoto(chale_id=chale_id, url=url)
             db.add(nova_foto)

             pass
    db.commit()
    db.refresh(chale)
    return chale
    
def excluir_chale(db, chale_id: int, anfitriao_id: int):
    
    chale = db.query(Chale).filter(Chale.id == chale_id, Chale.anfitriao_id == anfitriao_id).first()
    
    if not chale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chalé não encontrado."
        )
    reserva_existente = db.query(Reserva).filter(Reserva.chale_id == chale_id).first()
    
    if reserva_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este chalé possui histórico de reservas e não pode ser excluído permanentemente. Utilize a função de desativar."
        )
    db.delete(chale)
    db.commit()
    return {"mensagem": "Chalé excluído com sucesso do banco de dados."}
    
def deletar_foto_chale(db, chale_id: int, foto_id: int, anfitriao_id: int):
    chale = db.query(Chale).filter(Chale.id == chale_id, Chale.anfitriao_id == anfitriao_id).first()
    
    if not chale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chalé não encontrado ou você não tem permissão."
        )
    
    foto = db.query(ChaleFoto).filter(ChaleFoto.id == foto_id, ChaleFoto.chale_id == chale_id).first()
    
    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Foto não encontrada neste chalé."
        )
    
    db.delete(foto)
    db.commit()
    
    return {"mensagem": "Foto removida com sucesso!"}

    
    reserva_existente = db.query(Reserva).filter(Reserva.chale_id == chale_id).first()
    
    if reserva_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este chalé possui histórico de reservas e não pode ser excluído permanentemente. Utilize a função de desativar."
        )

    
    db.delete(chale)
    db.commit()
    return {"mensagem": "Chalé excluído com sucesso do banco de dados."}

def listar_chales(db: Session):
    return db.query(Chale).options(joinedload(Chale.fotos)).filter(Chale.ativo==True).all()

def listar_todos_chales(db: Session):
    return db.query(Chale).options(joinedload(Chale.fotos)).all()

def obter_chale_por_id(db: Session, chale_id: int):
    chale = db.query(Chale).options(joinedload(Chale.fotos)).filter(Chale.id == chale_id).first()

    if not chale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chalé não encontrado ou indisponível"
        )
    return chale