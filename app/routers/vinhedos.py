from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Vinhedo, VinhedoCreate, VinhedoRead

router = APIRouter(prefix="/vinhedos", tags=["Vinhedos"])

@router.post("/", response_model=VinhedoRead)
def criar_vinhedo(vinhedo: VinhedoCreate, session: Session = Depends(get_session)):
    db = Vinhedo.model_validate(vinhedo)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/", response_model=List[VinhedoRead])
def listar_vinhedos(session: Session = Depends(get_session)):
    return session.exec(select(Vinhedo).where(Vinhedo.ativo == True)).all()

@router.get("/{vinhedo_id}", response_model=VinhedoRead)
def buscar_vinhedo(vinhedo_id: int, session: Session = Depends(get_session)):
    v = session.get(Vinhedo, vinhedo_id)
    if not v or not v.ativo:
        raise HTTPException(status_code=404, detail="Vinhedo não encontrado")
    return v

@router.patch("/{vinhedo_id}", response_model=VinhedoRead)
def atualizar_vinhedo(vinhedo_id: int, dados: VinhedoCreate, session: Session = Depends(get_session)):
    v = session.get(Vinhedo, vinhedo_id)
    if not v or not v.ativo:
        raise HTTPException(status_code=404, detail="Vinhedo não encontrado")
    v.sqlmodel_update(dados.model_dump(exclude_unset=True))
    session.add(v)
    session.commit()
    session.refresh(v)
    return v

@router.delete("/{vinhedo_id}")
def inativar_vinhedo(vinhedo_id: int, session: Session = Depends(get_session)):
    v = session.get(Vinhedo, vinhedo_id)
    if not v or not v.ativo:
        raise HTTPException(status_code=404, detail="Vinhedo não encontrado")
    v.ativo = False
    session.add(v)
    session.commit()
    return {"message": f"Vinhedo '{v.nome}' inativado"}