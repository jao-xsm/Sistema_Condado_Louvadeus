from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class CadastroHospedeSchema(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)

    email: EmailStr

    senha: str = Field(..., min_length=6)

    telefone: str | None = None
    foto: str | None = None

    data_nascimento: date

    @field_validator('data_nascimento')
    @classmethod
    def verificar_maioridade(cls, valor_data: date) -> date:
        hoje = date.today()

        idade = hoje.year - valor_data.year - ((hoje.month, hoje.day) < (valor_data.month, valor_data.day))

        if idade < 18:
            raise ValueError("Apenas usuários com mais de 18 anos podem se cadastrar como hóspedes.")
        
        return valor_data
    
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str