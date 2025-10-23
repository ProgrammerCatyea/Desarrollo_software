from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from typing import List, Optional

Base = declarative_base()

juego_categoria = Table(
    "juego_categoria",
    Base.metadata,
    Column("juego_id", Integer, ForeignKey("juegos.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True),
)


class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)
    nivel = Column(String)

    juegos = relationship("Juego", back_populates="jugador")


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String)

    juegos = relationship(
        "Juego",
        secondary=juego_categoria,
        back_populates="categorias",
    )


class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    plataforma = Column(String)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))

    jugador = relationship("Jugador", back_populates="juegos")
    categorias = relationship(
        "Categoria",
        secondary=juego_categoria,
        back_populates="juegos",
    )


class JuegoEliminado(Base):
    __tablename__ = "juegos_eliminados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    plataforma = Column(String)
    jugador_id = Column(Integer)



class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    class Config:
        from_attributes = True


class CategoriaSchema(CategoriaBase):
    id: int
    class Config:
        from_attributes = True


class JugadorBase(BaseModel):
    nombre: str
    pais: Optional[str] = None
    nivel: Optional[str] = None
    class Config:
        from_attributes = True


class JugadorSchema(JugadorBase):
    id: int
    class Config:
        from_attributes = True


class JuegoBase(BaseModel):
    nombre: str
    plataforma: Optional[str] = None
    jugador_id: int
    categorias: List[str] = []
    class Config:
        from_attributes = True


class JuegoSchema(JuegoBase):
    id: int
    jugador: Optional[JugadorSchema] = None
    categorias: List[CategoriaSchema] = []
    class Config:
        from_attributes = True


class JuegoEliminadoSchema(BaseModel):
    id: int
    nombre: str
    plataforma: Optional[str]
    jugador_id: Optional[int]
    class Config:
        from_attributes = True
