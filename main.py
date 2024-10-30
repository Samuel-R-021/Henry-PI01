from fastapi import FastAPI
import pandas as pd

app = FastAPI()

func_dataset = pd.read_csv('full_funciones_dataset.csv')

# @app.get("/cantidad_filmaciones_mes/")
# async def cantidad_filmaciones_mes(mes: str = ''):
#     indice = func_dataset.index[func_dataset['title']== mes][0]
#     return f"La película {func_dataset['title'][indice]} fue estrenada en el año {func_dataset['release_year'][indice]} con un score/popularidad de {func_dataset['popularity'][indice]}"

# @app.get("/cantidad_filmaciones_dia/")
# async def cantidad_filmaciones_dia(dia: str = ''):
#     indice = func_dataset.index[func_dataset['title']== dia][0]
#     return f"La película {func_dataset['title'][indice]} fue estrenada en el año {func_dataset['release_year'][indice]} con un score/popularidad de {func_dataset['popularity'][indice]}"

@app.get("/score_titulo/")
async def score_titulo(title: str = ''):
    indice = func_dataset.index[func_dataset['title']== title][0]  # El index da una tupla, donde el primer valor es el indice y el segungo el tipo de dato
    return f"La película {func_dataset['title'][indice]} fue estrenada en el año {func_dataset['release_year'][indice]} con un score/popularidad de {func_dataset['popularity'][indice]}"
    
@app.get("/votos_titulo/")
async def votos_titulo(title: str = ''):
    indice = func_dataset.index[func_dataset['title']== title][0]
    return f"La película {func_dataset['title'][indice]} no tiene al menos 2000 valoraciones, por lo que no se devuelve ningun valor." if func_dataset['vote_count'][indice] < 2000 else f"La película {func_dataset['title'][indice]} fue estrenada en el año {func_dataset['release_year'][indice]}. La misma cuenta con un total de {int(func_dataset['vote_count'][indice])} valoraciones, con un promedio de {func_dataset['vote_average'][indice]}"