from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum as PyEnum
from datetime import datetime

# ─────────────────────────────────────────
# CASTA
# ─────────────────────────────────────────
class CastaBase(SQLModel):
    """Campos compartilhados entre criação e leitura."""
    nome: str = Field(min_length=2, max_length=100)
    origem: Optional[str] = Field(default=None, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=500)
    ativo: bool = Field(default=True)

class Casta(CastaBase, table=True):
    """Tabela real no banco."""
    id: Optional[int] = Field(default=None, primary_key=True)
    plantios: List["Plantio"] = Relationship(back_populates="casta")

class CastaCreate(CastaBase):
    pass

class CastaRead(CastaBase):
    id: int


# ─────────────────────────────────────────
# VINHEDO
# ─────────────────────────────────────────
class VinhedoBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    localizacao: Optional[str] = Field(default=None, max_length=200)
    area_total_hectares: Optional[float] = Field(default=None, gt=0)
    ativo: bool = Field(default=True)

class Vinhedo(VinhedoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parcelas: List["Parcela"] = Relationship(back_populates="vinhedo")

class VinhedoCreate(VinhedoBase):
    pass

class VinhedoRead(VinhedoBase):
    id: int


# ─────────────────────────────────────────
# PARCELA
# ─────────────────────────────────────────
class ParcelaBase(SQLModel):
    nome: str = Field(min_length=1, max_length=100)
    area_hectares: Optional[float] = Field(default=None, gt=0)
    tipo_solo: Optional[str] = Field(default=None, max_length=100)
    orientacao: Optional[str] = Field(default=None, max_length=50)
    ativo: bool = Field(default=True)

class Parcela(ParcelaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vinhedo_id: int = Field(foreign_key="vinhedo.id")
    vinhedo: Optional[Vinhedo] = Relationship(back_populates="parcelas")
    plantios: List["Plantio"] = Relationship(back_populates="parcela")

class ParcelaCreate(ParcelaBase):
    vinhedo_id: int

class ParcelaRead(ParcelaBase):
    id: int
    vinhedo_id: int


# ─────────────────────────────────────────
# PLANTIO
# ─────────────────────────────────────────
class PlantioBase(SQLModel):
    data_plantio: str = Field(
        description="Data no formato AAAA-MM-DD"
    )
    quantidade_mudas: Optional[int] = Field(default=None, gt=0)
    espaco_entre_plantas_m: Optional[float] = Field(default=None, gt=0)
    observacao: Optional[str] = Field(default=None, max_length=500)
    ativo: bool = Field(default=True)

class Plantio(PlantioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parcela_id: int = Field(foreign_key="parcela.id")
    casta_id: int = Field(foreign_key="casta.id")
    parcela: Optional[Parcela] = Relationship(back_populates="plantios")
    casta: Optional[Casta] = Relationship(back_populates="plantios")

class PlantioCreate(PlantioBase):
    parcela_id: int
    casta_id: int

class PlantioRead(PlantioBase):
    id: int
    parcela_id: int
    casta_id: int

class NivelAcesso(str, PyEnum):
    ADMIN = "ADMIN"      
    OPERADOR = "OPERADOR"  
    CONSULTA = "CONSULTA"  

class UsuarioBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(unique=True, max_length=200)
    nivel: NivelAcesso = Field(default=NivelAcesso.OPERADOR)
    ativo: bool = Field(default=True)

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    senha_hash: str 
    criado_em: datetime = Field(default_factory=datetime.utcnow)

class UsuarioCreate(SQLModel):
    nome: str
    email: str
    senha: str 
    nivel: NivelAcesso = NivelAcesso.OPERADOR

class UsuarioRead(UsuarioBase):
    id: int
    criado_em: datetime 