from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    email:Optional[str]=None

class UsuarioCrear(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int