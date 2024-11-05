from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

func_1_4_dataset = pd.read_csv('funciones_1_4_dataset.csv', index_col='lowercase_title')
func_5_6_dataset = pd.read_csv('funciones_5_6_dataset.csv')
cast_dataset = pd.read_csv('cast_credits.csv',index_col='lowercase_name')
crew_dataset = pd.read_csv('crew_credits.csv',index_col='lowercase_name')
modelo_dataset = pd.read_csv('modelo_database.csv')

cv = CountVectorizer(max_features=3500, stop_words='english')
vector = cv.fit_transform(modelo_dataset['tags']).toarray()
similitud = cosine_similarity(vector)

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
async def score_titulo(titulo_de_la_filmacion: str = ''):
    indice = titulo_de_la_filmacion.lower()
    return f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]} con un score/popularidad de {func_1_4_dataset['popularity'][indice]}"
    
@app.get("/votos_titulo/")
async def votos_titulo(titulo_de_la_filmacion: str = ''):
    indice = titulo_de_la_filmacion.lower()
    return f"La película {func_1_4_dataset['title'][indice]} tiene menos de 2000 valoraciones, por lo que no se devuelve ningun valor." if func_1_4_dataset['vote_count'][indice] < 2000 else f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]}. La misma cuenta con un total de {int(func_1_4_dataset['vote_count'][indice])} valoraciones, con un promedio de {func_1_4_dataset['vote_average'][indice]}"

@app.get("/get_actor/")
async def get_actor(nombre_actor: str = ''):
    
    # convertir a minuscula para evitar errores, y usar como indice en el cast_dataset
    indice = nombre_actor.lower()
    

    # aqui tomamos los id sacados de cast_dataset y buscamos cuales se encuentran en el dataset de movies (func_5_6_dataset)
    # y nos quedamos solo con los que SI estan en el datasets de movies.
    movies_cast_id_match = func_5_6_dataset['id'].isin(cast_dataset['id'][indice])

    # valores a extraer para el resultado de la funcion
    nombre = cast_dataset['name'][indice][0]
    filmaciones = func_5_6_dataset['id'][movies_cast_id_match].shape[0]
    retorno = func_5_6_dataset['return'][movies_cast_id_match].sum()
    promedio = retorno/filmaciones
    return f"El actor {nombre} ha participado en {filmaciones} filmaciones, el mismo ha conseguido un retorno de {round(retorno,ndigits=2)} con un promedio de {round(promedio, ndigits=2)} por filmacion."

@app.get("/get_director/")
async def get_director(nombre_actor: str = ''):
    indice = nombre_actor.lower()
    
    movies_crew_id_match = func_5_6_dataset['id'].isin(crew_dataset['id'][indice])

    nombre = crew_dataset['name'][indice][0]
    filmaciones = func_5_6_dataset['id'][movies_crew_id_match]
    retorno = func_5_6_dataset['return'][movies_crew_id_match].sum()
    promedio = retorno/filmaciones.shape[0]
    return f"El director {nombre} ha dirigido {filmaciones.shape[0]} filmaciones, con un retorno total de {round(retorno,ndigits=2)}, siendo un promedio de {round(promedio, ndigits=2)} por filmacion."

@app.get("/recomendacion/")
async def recomendacion(titulo: str = ''):
    
    # cv = CountVectorizer(stop_words='english')
    # vector = cv.fit_transform(modelo_dataset['tags']).toarray()
    # similitud = cosine_similarity(vector)

    indice = modelo_dataset[modelo_dataset['title']== titulo].index[0]

    distancia = sorted(list(enumerate(similitud[indice])), reverse=True, key=lambda x: x[1])

    # for i in distancia[1:6]:
    #     print(modelo_dataset.iloc[i[0]].title)
    return [modelo_dataset.iloc[i[0]].title for i in distancia[1:6]]
