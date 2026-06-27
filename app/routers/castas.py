from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Casta, CastaCreate, CastaRead

router = APIRouter(prefix="/castas", tags=["Castas"])

@router.post("/", response_model=CastaRead)
def criar_casta(casta: CastaCreate, session: Session = Depends(get_session)):
    db_casta = Casta.model_validate(casta)
    session.add(db_casta)
    session.commit()
    session.refresh(db_casta)
    return db_casta

@router.get("/", response_model=List[CastaRead])
def listar_castas(session: Session = Depends(get_session)):
    castas = session.exec(select(Casta).where(Casta.ativo == True)).all()
    return castas

@router.get("/{casta_id}", response_model=CastaRead)
def buscar_casta(casta_id: int, session: Session = Depends(get_session)):
    casta = session.get(Casta, casta_id)
    if not casta or not casta.ativo:
        raise HTTPException(status_code=404, detail="Casta não encontrada")
    return casta

@router.patch("/{casta_id}", response_model=CastaRead)
def atualizar_casta(casta_id: int, dados: CastaCreate, session: Session = Depends(get_session)):
    casta = session.get(Casta, casta_id)
    if not casta or not casta.ativo:
        raise HTTPException(status_code=404, detail="Casta não encontrada")
    dados_dict = dados.model_dump(exclude_unset=True)
    casta.sqlmodel_update(dados_dict)
    session.add(casta)
    session.commit()
    session.refresh(casta)
    return casta

@router.delete("/{casta_id}")
def inativar_casta(casta_id: int, session: Session = Depends(get_session)):
    """Exclusão lógica — nunca apaga do banco (regra R10)."""
    casta = session.get(Casta, casta_id)
    if not casta or not casta.ativo:
        raise HTTPException(status_code=404, detail="Casta não encontrada")
    casta.ativo = False
    session.add(casta)
    session.commit()
    return {"message": f"Casta '{casta.nome}' inativada com sucesso"}