from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import hash_senha, verificar_senha, criar_token
from app.database import get_session
from app.dependencies import get_current_user
from app.models import Usuario, UsuarioCreate, UsuarioRead

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    usuario = session.exec(
        select(Usuario).where(Usuario.email == form.username)
    ).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
        )
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo. Contate o administrador.",
        )
    token = criar_token({"sub": usuario.email, "nivel": usuario.nivel})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/usuarios", response_model=UsuarioRead)
def criar_usuario(
    dados: UsuarioCreate,
    session: Session = Depends(get_session),
    _admin: Usuario = Depends(get_current_user),
):
    existente = session.exec(
        select(Usuario).where(Usuario.email == dados.email)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        nivel=dados.nivel,
        senha_hash=hash_senha(dados.senha),
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.get("/me", response_model=UsuarioRead)
def meu_perfil(usuario: Usuario = Depends(get_current_user)):
    return usuario