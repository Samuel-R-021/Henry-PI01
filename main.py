from fastapi import FastAPI
import pandas as pd

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
popularity_test = pd.read_csv('popularity_test.csv')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/inicio")
async def ruta_prueba():
    return "Hola"

@app.get("/prueba")
async def prueba():
    return "Probando el consumo de la API"

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/score_titulo/")
async def score_titulo(title: str = ''):
    indice = popularity_test.index[popularity_test['title']== title][0]
    return print(f"La película {popularity_test['title'][indice]} fue estrenada en el año {popularity_test['release_year'][indice]} con un score/popularidad de {popularity_test['popularity'][indice]}")
    