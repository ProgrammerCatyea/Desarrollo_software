from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel

Base = declarative_base()


juego_categoria = Table(
    "juego_categoria",
    Base.metadata,
    Column("juego_id", Integer, ForeignKey("juegos.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True)
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

    # Relación N:M con Juego
    juegos = relationship(
        "Juego",
        secondary=juego_categoria,
        back_populates="categorias"
    )



class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    plataforma = Column(String)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))

    # Relaciones
    jugador = relationship("Jugador", back_populates="juegos")
    categorias = relationship(
        "Categoria",
        secondary=juego_categoria,
        back_populates="juegos"
    )




class CategoriaSchema(BaseModel):
    id: int | None = None
    nombre: str
    descripcion: str | None = None

    class Config:
        orm_mode = True


class JugadorSchema(BaseModel):
    id: int | None = None
    nombre: str
    pais: str | None = None
    nivel: str | None = None

    class Config:
        orm_mode = True


class JuegoSchema(BaseModel):
    id: int | None = None
    nombre: str
    plataforma: str | None = None
    jugador_id: int | None = None
    categorias: list[CategoriaSchema] | None = []

    class Config:
        orm_mode = True
