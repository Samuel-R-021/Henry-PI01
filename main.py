from fastapi import FastAPI

app = FastAPI()


@app.get("/inicio")
async def ruta_prueba():
    return "Hola"

@app.get("/prueba")
async def prueba():
    return "Probando el consumo de la API"