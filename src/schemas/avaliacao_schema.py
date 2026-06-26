from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AvaliacaoCreate(BaseModel):
    chale_id: int
    
    nota: int = Field(ge=0, le=5, description="Nota de 0 a 5 estrelas")
    comentario: Optional[str] = None

class AvaliacaoResponse(BaseModel):
    id: int
    nome_hospede: str 
    nota: int
    comentario: Optional[str]
    data_criacao: datetime

    class Config:
        from_attributes = True