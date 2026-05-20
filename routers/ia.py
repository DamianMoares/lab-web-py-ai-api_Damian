from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional
from datetime import datetime
from database import fake_db_usuarios, fake_db_notas
from dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["IA"], dependencies=[Depends(get_current_user)])

# historial de chat por sesión
sesiones_chat = {}


@router.post("/chat")
def chat(data: dict, username: str = Depends(get_current_user)):
    session_id = data.get("session_id", "default")
    message = data.get("mensaje", "")

    if not message:
        raise HTTPException(status_code=400, detail="Falta mensaje")

    if session_id not in sesiones_chat:
        sesiones_chat[session_id] = []

    sesiones_chat[session_id].append({
        "role": "user",
        "content": message,
        "timestamp": datetime.utcnow().isoformat(),
    })

    # respuesta simulada de IA
    respuesta = {
        "role": "assistant",
        "content": f"[Simulación IA] He entendido tu mensaje: '{message}'.",
        "timestamp": datetime.utcnow().isoformat(),
    }

    sesiones_chat[session_id].append(respuesta)

    return {"respuesta": respuesta["content"], "session_id": session_id}


@router.get("/chat/history/{session_id}")
def obtener_historial(session_id: str, username: str = Depends(get_current_user)):
    if session_id not in sesiones_chat:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"historial": sesiones_chat[session_id]}


@router.get("/search")
def buscar_notas(q: str, username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]

    resultados = [
        n for n in fake_db_notas
        if n.usuario_id == usuario_id
        and (q.lower() in n.titulo.lower() or q.lower() in n.contenido.lower())
    ]

    return {"resultados": resultados}


@router.get("/context")
def obtener_contexto(username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]
    num_notas = len([n for n in fake_db_notas if n.usuario_id == usuario_id])

    return {
        "mensaje": "Esta API permite gestionar notas de texto y permitir interacción con un agente de IA.",
        "endpoints": [
            "POST /auth/registro",
            "POST /auth/login",
            "GET /notas",
            "POST /notas",
            "PUT /notas/{id}",
            "DELETE /notas/{id}",
            "POST /api/chat",
            "GET /api/chat/history/{session_id}",
            "GET /api/search?q=...",
            "GET /api/context",
            "POST /api/resumir/{nota_id}"
        ],
        "usuario": username,
        "numero_notas_usuario": num_notas,
    }


@router.post("/resumir/{nota_id}")
def resumir_nota(nota_id: int, username: str = Depends(get_current_user)):
    usuario_id = fake_db_usuarios[username]["id"]

    nota = None
    for n in fake_db_notas:
        if n.id == nota_id and n.usuario_id == usuario_id:
            nota = n

    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada o no es tuya")

    resumen = f"Esta nota titulada '{nota.titulo}' trata sobre: {nota.contenido[:100]}... (continúa)"
    return {"resumen": resumen, "nota_id": nota_id}