from fastapi import FastAPI, HTTPException
from typing import List
import json
from modelos import Juego, Jugador, Categoria

app = FastAPI(title="Proyecto de Videojuegos", version="1.0")


DATA_FILE = "data/juegos.json"


def cargar_datos():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


juegos = cargar_datos()



@app.get("/juegos", response_model=List[Juego])
def obtener_juegos():
    """Obtener todos los juegos."""
    return juegos


@app.get("/juegos/{juego_id}", response_model=Juego)
def obtener_juego_por_id(juego_id: int):
    """Obtener un juego específico por su ID."""
    for juego in juegos:
        if juego["id"] == juego_id:
            return juego
    raise HTTPException(status_code=404, detail="Juego no encontrado")


@app.post("/juegos", response_model=Juego)
def crear_juego(juego: Juego):
    """Crear un nuevo juego."""
    nuevo_id = max([j["id"] for j in juegos], default=0) + 1
    nuevo_juego = juego.dict()
    nuevo_juego["id"] = nuevo_id
    juegos.append(nuevo_juego)
    guardar_datos(juegos)
    return nuevo_juego


@app.put("/juegos/{juego_id}", response_model=Juego)
def actualizar_juego(juego_id: int, juego_actualizado: Juego):
    """Actualizar un juego existente por ID."""
    for index, juego in enumerate(juegos):
        if juego["id"] == juego_id:
            actualizado = juego_actualizado.dict()
            actualizado["id"] = juego_id  
            juegos[index] = actualizado
            guardar_datos(juegos)
            return actualizado
    raise HTTPException(status_code=404, detail="Juego no encontrado")


@app.delete("/juegos/{juego_id}")
def eliminar_juego(juego_id: int):
    """Eliminar un juego por ID."""
    for index, juego in enumerate(juegos):
        if juego["id"] == juego_id:
            juegos.pop(index)
            guardar_datos(juegos)
            return {"mensaje": f"Juego con ID {juego_id} eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Juego no encontrado")
