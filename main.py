from fastapi import FastAPI
import pandas as pd

app = FastAPI()

popularity_test = pd.read_csv('popularity_test.csv')

@app.get("/score_titulo/")
async def score_titulo(title: str = ''):
    indice = popularity_test.index[popularity_test['title']== title][0]
    return f"La película {popularity_test['title'][indice]} fue estrenada en el año {popularity_test['release_year'][indice]} con un score/popularidad de {popularity_test['popularity'][indice]}"
    