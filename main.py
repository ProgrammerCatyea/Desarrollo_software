from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from modelos import Base, Juego, Jugador, Categoria, JuegoSchema, JugadorSchema, CategoriaSchema


app = FastAPI(title="Proyecto de Videojuegos", version="2.0")

DATABASE_URL = "sqlite:///./data/juegos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/juegos", response_model=List[JuegoSchema])
def obtener_juegos(db: Session = Depends(get_db)):
    return db.query(Juego).all()

@app.get("/juegos/{juego_id}", response_model=JuegoSchema)
def obtener_juego_por_id(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego

@app.post("/juegos", response_model=JuegoSchema)
def crear_juego(juego: JuegoSchema, db: Session = Depends(get_db)):
    nuevo_juego = Juego(nombre=juego.nombre, plataforma=juego.plataforma, jugador_id=juego.jugador_id)
    db.add(nuevo_juego)
    db.commit()
    db.refresh(nuevo_juego)
    return nuevo_juego

@app.put("/juegos/{juego_id}", response_model=JuegoSchema)
def actualizar_juego(juego_id: int, juego_actualizado: JuegoSchema, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    juego.nombre = juego_actualizado.nombre
    juego.plataforma = juego_actualizado.plataforma
    juego.jugador_id = juego_actualizado.jugador_id
    db.commit()
    db.refresh(juego)
    return juego

@app.delete("/juegos/{juego_id}")
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    db.delete(juego)
    db.commit()
    return {"mensaje": f"Juego con ID {juego_id} eliminado correctamente"}



@app.get("/jugadores", response_model=List[JugadorSchema])
def obtener_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()

@app.post("/jugadores", response_model=JugadorSchema)
def crear_jugador(jugador: JugadorSchema, db: Session = Depends(get_db)):
    nuevo_jugador = Jugador(nombre=jugador.nombre, pais=jugador.pais, nivel=jugador.nivel)
    db.add(nuevo_jugador)
    db.commit()
    db.refresh(nuevo_jugador)
    return nuevo_jugador



@app.get("/categorias", response_model=List[CategoriaSchema])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.post("/categorias", response_model=CategoriaSchema)
def crear_categoria(categoria: CategoriaSchema, db: Session = Depends(get_db)):
    nueva_categoria = Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria
