from pydantic import BaseModel, Field
from typing import List, Optional

class ChaleFotoSchema(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True

class ChaleBase(BaseModel):
    nome: str = Field(..., min_length=5, max_length=100, description="Nome do chalé")
    descricao: str = Field(..., min_length=15, description="Descrição detalhada do chalé")

    val_diaria: float = Field(..., gt=0, description="Valor da diária do chalé")
    quant_camas: int = Field(..., ge=1, description="Quantidade de camas no chalé")

    foto_capa: Optional[str] = None
    galeria_fotos: List[str] = []

    ativo: bool = True

class ChaleCreate(ChaleBase):
    
    #anfitriao_id: int = Field(..., description="campo temporario enquanto nao temos front para colocar o id do anfitrião")#deletar no futuro

    pass


class ChaleResponse(ChaleBase):
    id: int
    anfitriao_id: int
    nome: str
    descricao: str
    val_diaria: float
    quant_camas: int
    ativo: bool
    foto_capa: Optional[str]
    galeria_fotos: List[ChaleFotoSchema] = []

    class Config:
        from_attributes = True