from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from models.usuario import UsuarioCrear, Usuario
from auth.jwt import hash_password, crear_token_acceso, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

# base de datos de usuarios en memoria
fake_db_usuarios = {}
_next_user_id = 1


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/registro", response_model=Usuario)
def registro(usuario: UsuarioCrear):
    if usuario.username in fake_db_usuarios:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    global _next_user_id

    usuario_hashed = Usuario(
        id=_next_user_id,
        username=usuario.username,
        email=usuario.email,
    )

    fake_db_usuarios[usuario.username] = {
        "id": usuario_hashed.id,
        "username": usuario.username,
        "email": usuario.email,
        "hashed_password": hash_password(usuario.password),
    }
    _next_user_id += 1
    return usuario_hashed


@router.post("/login", response_model=Token)
def login(usuario: UsuarioCrear):
    db_user = fake_db_usuarios.get(usuario.username)
    if not db_user or not verify_password(usuario.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Nombre o contraseña incorrectos")

    access_token = crear_token_acceso(
        data={"sub": usuario.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}