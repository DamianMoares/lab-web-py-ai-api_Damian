from fastapi import APIRouter, Depends, HTTPException, status
from models.nota import NotaCrear, Nota
from typing import Optional, List
from datetime import datetime
from database import fake_db_usuarios, fake_db_notas
from dependencies import get_current_user

router = APIRouter(prefix="/notas", tags=["notas"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[Nota])
def obtener_notas(
    buscar: Optional[str] = None,
    username: str = Depends(get_current_user),
):
    # solo notas del usuario logueado
    usuario_id = fake_db_usuarios[username]["id"]
    mis_notas = [n for n in fake_db_notas if n.usuario_id == usuario_id]

    # filtrar por texto si viene buscar
    if buscar:
        mis_notas = [
            n for n in mis_notas
            if buscar.lower() in n.titulo.lower() or buscar.lower() in n.contenido.lower()
        ]

    return mis_notas


@router.get("/{id}", response_model=Nota)
def obtener_nota(id: int, username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]

    for n in fake_db_notas:
        if n.id == id:
            if n.usuario_id == usuario_id:
                return n
    raise HTTPException(status_code=404, detail="Nota no encontrada")


_next_nota_id = 1


@router.post("/", response_model=Nota)
def crear_nota(nota: NotaCrear, username: str = Depends(get_current_user)):
    global _next_nota_id

    usuario = fake_db_usuarios[username]

    nota_completa = Nota(
        id=_next_nota_id,
        titulo=nota.titulo,
        contenido=nota.contenido,
        usuario_id=usuario["id"],
        creada_en=datetime.utcnow(),
        actualizada_en=None,
    )
    fake_db_notas.append(nota_completa)
    _next_nota_id += 1
    return nota_completa


@router.put("/{id}", response_model=Nota)
def actualizar_nota(id: int, nota: NotaCrear, username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]

    for n in fake_db_notas:
        if n.id == id:
            if n.usuario_id != usuario_id:
                raise HTTPException(status_code=403, detail="No es tu nota")

            n.titulo = nota.titulo
            n.contenido = nota.contenido
            n.actualizada_en = datetime.utcnow()
            return n

    raise HTTPException(status_code=404, detail="Nota no encontrada")


@router.delete("/{id}")
def borrar_nota(id: int, username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]

    for i, n in enumerate(fake_db_notas):
        if n.id == id:
            if n.usuario_id != usuario_id:
                raise HTTPException(status_code=403, detail="No es tu nota")
            fake_db_notas.pop(i)
            return {"mensaje": "Nota eliminada"}

    raise HTTPException(status_code=404, detail="Nota no encontrada")