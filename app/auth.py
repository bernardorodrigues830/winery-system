from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.config import settings
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

class Tokendata(BaseModel)
email: Optional[str] = None
nivel: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    nivel: Optional[str] = None

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hash)

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expiracao})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decodificar_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        nivel: str = payload.get("nivel")
        if email is None:
            return None
        return TokenData(email=email, nivel=nivel)
    except JWTError:
        return None