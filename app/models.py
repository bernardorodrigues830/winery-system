from typing import Optional
from sqlmodel import Field, SQLModel

class CastaBase(SQLModel):
    """Campos compartilhados entre criação e leitura."""
    nome: str = Field(min_length=2, max_length=100)
    origem: Optional[str] = Field(default=None, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=500)
    ativo: bool = Field(default=True)

class Casta(CastaBase, table=True):
    """Tabela real no banco."""
    id: Optional[int] = Field(default=None, primary_key=True)

class CastaCreate(CastaBase):
    """Schema para receber dados na criação (sem id)."""
    pass

class CastaRead(CastaBase):
    """Schema para devolver dados (com id)."""
    id: int