from pydantic import BaseModel
from typing import List, Optional


class Categoria(BaseModel):
    id: int
    nombre: str


class Jugador(BaseModel):
    id: int
    nombre: str
    correo: str


class Juego(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    categorias: List[Categoria]
    jugadores: List[Jugador]
