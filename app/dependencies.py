from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.auth import decodificar_token
from app.database import get_session
from app.models import Usuario, NivelAcesso

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Usuario:
    credencial_invalida = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado. Faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    dados = decodificar_token(token)
    if dados is None:
        raise credencial_invalida
    usuario = session.exec(
        select(Usuario).where(Usuario.email == dados.email)
    ).first()
    if not usuario or not usuario.ativo:
        raise credencial_invalida
    return usuario

def requer_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.nivel != NivelAcesso.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )
    return usuario

def requer_operador(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.nivel == NivelAcesso.CONSULTA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seu perfil não tem permissão para esta operação.",
        )
    return usuario