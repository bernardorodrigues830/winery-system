from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Plantio, PlantioCreate, PlantioRead, Parcela, Casta

router = APIRouter(prefix="/plantios", tags=["Plantios"])

@router.post("/", response_model=PlantioRead)
def criar_plantio(plantio: PlantioCreate, session: Session = Depends(get_session)):
    # Regra R4: parcela e casta precisam existir
    parcela = session.get(Parcela, plantio.parcela_id)
    if not parcela or not parcela.ativo:
        raise HTTPException(status_code=404, detail="Parcela não encontrada")

    casta = session.get(Casta, plantio.casta_id)
    if not casta or not casta.ativo:
        raise HTTPException(status_code=404, detail="Casta não encontrada")

    db = Plantio.model_validate(plantio)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/", response_model=List[PlantioRead])
def listar_plantios(
    parcela_id: int | None = None,
    casta_id: int | None = None,
    session: Session = Depends(get_session)
):
    query = select(Plantio).where(Plantio.ativo == True)
    if parcela_id:
        query = query.where(Plantio.parcela_id == parcela_id)
    if casta_id:
        query = query.where(Plantio.casta_id == casta_id)
    return session.exec(query).all()

@router.get("/{plantio_id}", response_model=PlantioRead)
def buscar_plantio(plantio_id: int, session: Session = Depends(get_session)):
    p = session.get(Plantio, plantio_id)
    if not p or not p.ativo:
        raise HTTPException(status_code=404, detail="Plantio não encontrado")
    return p

@router.delete("/{plantio_id}")
def inativar_plantio(plantio_id: int, session: Session = Depends(get_session)):
    p = session.get(Plantio, plantio_id)
    if not p or not p.ativo:
        raise HTTPException(status_code=404, detail="Plantio não encontrado")
    p.ativo = False
    session.add(p)
    session.commit()
    return {"message": f"Plantio id={p.id} inativado"}