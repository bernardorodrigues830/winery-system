from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Parcela, ParcelaCreate, ParcelaRead, Vinhedo

router = APIRouter(prefix="/parcelas", tags=["Parcelas"])

@router.post("/", response_model=ParcelaRead)
def criar_parcela(parcela: ParcelaCreate, session: Session = Depends(get_session)):
    vinhedo = session.get(Vinhedo, parcela.vinhedo_id)
    if not vinhedo or not vinhedo.ativo:
        raise HTTPException(status_code=404, detail="Vinhedo não encontrado")
    db = Parcela.model_validate(parcela)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/", response_model=List[ParcelaRead])
def listar_parcelas(vinhedo_id: int | None = None, session: Session = Depends(get_session)):
    query = select(Parcela).where(Parcela.ativo == True)
    if vinhedo_id:
        query = query.where(Parcela.vinhedo_id == vinhedo_id)
    return session.exec(query).all()

@router.get("/{parcela_id}", response_model=ParcelaRead)
def buscar_parcela(parcela_id: int, session: Session = Depends(get_session)):
    p = session.get(Parcela, parcela_id)
    if not p or not p.ativo:
        raise HTTPException(status_code=404, detail="Parcela não encontrada")
    return p

@router.patch("/{parcela_id}", response_model=ParcelaRead)
def atualizar_parcela(parcela_id: int, dados: ParcelaCreate, session: Session = Depends(get_session)):
    p = session.get(Parcela, parcela_id)
    if not p or not p.ativo:
        raise HTTPException(status_code=404, detail="Parcela não encontrada")
    p.sqlmodel_update(dados.model_dump(exclude_unset=True))
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@router.delete("/{parcela_id}")
def inativar_parcela(parcela_id: int, session: Session = Depends(get_session)):
    p = session.get(Parcela, parcela_id)
    if not p or not p.ativo:
        raise HTTPException(status_code=404, detail="Parcela não encontrada")
    p.ativo = False
    session.add(p)
    session.commit()
    return {"message": f"Parcela '{p.nome}' inativada"}