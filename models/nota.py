from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotaBase(BaseModel):
    titulo: str
    contenido: str


class NotaCrear(NotaBase):
    pass


class Nota(NotaBase):
    id: int
    usuario_id: int
    creada_en: datetime
    actualizada_en: Optional[datetime] = None