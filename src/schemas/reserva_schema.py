from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional

class ReservaCreate(BaseModel):
    chale_id: int
    data_checkin: date
    data_checkout: date

    @model_validator(mode="after")
    def verificar_consistencia_datas(self)-> "ReservaCreate":
        hoje = date.today()

        if self.data_checkin < hoje:
            raise ValueError("A data de check-in não pode ser menor que a data de hoje.")
        
        if self.data_checkout <= self.data_checkin:
            raise ValueError("A data de check-out deve ser posterior à data de check-in.")
        
        return self
    
class ReservaUpdate(BaseModel):
    data_checkin: date
    data_checkout: date

    @model_validator(mode="after")
    def verificar_consistencia_datas(self) -> "ReservaUpdate":
        hoje = date.today()

        if self.data_checkin < hoje:
            raise ValueError("A nova data de check-in não pode ser no passado.")
        
        if self.data_checkout <= self.data_checkin:
            raise ValueError("A nova data de check-out deve ser posterior à data de check-in.")
        
        return self
class ReservaResponse(BaseModel):
    id: int
    hospede_id: int
    chale_id: int
    data_checkin: date
    data_checkout: date
    valor_total: float
    status: str

    class Config:
        from_attributes = True

class ReservaCalendario(BaseModel):
    id: int
    chale__id: int
    data_checkin: date
    data_checkout: date

    class Config:
        from_attributes = True

class DisponibilidadeChale(BaseModel):
    data_checkin: date
    data_checkout: date

    class Config:
        from_attributes = True