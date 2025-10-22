from pydantic import BaseModel
from typing import List, Optional

class Jugador(BaseModel):
    nombre: str
    nivel: Optional[int] = 1
    horas_juego: Optional[int] = 0

class Categoria(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class Juego(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    categorias: List[str] = []
    jugadores: List[str] = []
