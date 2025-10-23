from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./videojuegos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

 
    jugador = relationship("Jugador", back_populates="juegos")
    categorias = relationship(
        "Categoria",
        secondary=juego_categoria,
        back_populates="juegos"
    )



class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True


class JugadorBase(BaseModel):
    nombre: str
    pais: str | None = None
    nivel: str | None = None

    class Config:
        from_attributes = True


class JuegoBase(BaseModel):
    nombre: str
    plataforma: str | None = None
    jugador_id: int
    categorias: list[str] = []

    class Config:
        from_attributes = True
