from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from modelos import Base, Juego, Jugador, Categoria, juego_categoria
from typing import List
import csv

DATABASE_URL = "sqlite:///data/juegos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proyecto de Videojuegos", version="2.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/juegos", response_model=List[Juego])
def obtener_juegos(db: Session = Depends(get_db)):
    return db.query(Juego).all()

@app.get("/juegos/{juego_id}", response_model=Juego)
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego

@app.post("/juegos", response_model=Juego)
def crear_juego(juego: Juego, db: Session = Depends(get_db)):
    db.add(juego)
    db.commit()
    db.refresh(juego)
    return juego

@app.put("/juegos/{juego_id}", response_model=Juego)
def actualizar_juego(juego_id: int, datos: Juego, db: Session = Depends(get_db)):
    juego = db.query(Juego).filter(Juego.id == juego_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    for key, value in datos.dict().items():
        setattr(juego, key, value)
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
    return {"mensaje": "Juego eliminado correctamente"}


@app.get("/jugadores", response_model=List[Jugador])
def obtener_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()

@app.post("/jugadores", response_model=Jugador)
def crear_jugador(jugador: Jugador, db: Session = Depends(get_db)):
    db.add(jugador)
    db.commit()
    db.refresh(jugador)
    return jugador


@app.get("/categorias", response_model=List[Categoria])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.post("/categorias", response_model=Categoria)
def crear_categoria(categoria: Categoria, db: Session = Depends(get_db)):
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@app.get("/juegos/buscar/{nombre}", response_model=List[Juego])
def buscar_juego_por_nombre(nombre: str, db: Session = Depends(get_db)):
    juegos = db.query(Juego).filter(Juego.nombre.ilike(f"%{nombre}%")).all()
    if not juegos:
        raise HTTPException(status_code=404, detail="No se encontraron juegos con ese nombre")
    return juegos


@app.get("/reporte")
def generar_reporte(db: Session = Depends(get_db)):
    juegos = db.query(Juego).all()
    with open("report/reporte.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nombre", "Plataforma", "Categoría"])
        for juego in juegos:
            writer.writerow([juego.id, juego.nombre, juego.plataforma, juego.categoria_id])
    return {"mensaje": "Reporte generado exitosamente"}
