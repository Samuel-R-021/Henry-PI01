from fastapi import FastAPI
import pandas as pd

app = FastAPI()

func_1_4_dataset = pd.read_csv('funciones_1_4_dataset.csv', index_col='lowercase_title')

@app.get("/cantidad_filmaciones_mes/")
async def cantidad_filmaciones_mes(mes: str = ''):
    total = func_1_4_dataset['month_name'][func_1_4_dataset['month_name']== mes.capitalize()].count()
    return f'{total} películas fueron estrenadas en el mes de {mes.lower()}'

@app.get("/cantidad_filmaciones_dia/")
async def cantidad_filmaciones_dia(dia: str = ''):
    if dia.lower() == 'miercoles':
        dia = 'miércoles'
    elif dia.lower() == 'sabado':
        dia = 'sábado'
    total = func_1_4_dataset['day_name'][func_1_4_dataset['day_name']== dia.capitalize()].count()
    return f'{total} películas fueron estrenadas en los días {dia.lower()}'

@app.get("/score_titulo/")
async def score_titulo(title: str = ''):
    indice = title.lower()
    return f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]} con un score/popularidad de {func_1_4_dataset['popularity'][indice]}"
    
@app.get("/votos_titulo/")
async def votos_titulo(title: str = ''):
    indice = title.lower()
    return f"La película {func_1_4_dataset['title'][indice]} no tiene al menos 2000 valoraciones, por lo que no se devuelve ningun valor." if func_1_4_dataset['vote_count'][indice] < 2000 else f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]}. La misma cuenta con un total de {int(func_1_4_dataset['vote_count'][indice])} valoraciones, con un promedio de {func_1_4_dataset['vote_average'][indice]}"