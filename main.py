from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel

app = FastAPI()

# donde esta index_col=, se hizo para escoger dicha columna como indice para simplificar las correspondientes busquedas
func_1_4_dataset = pd.read_csv('funciones_1_4_dataset.csv', index_col='lowercase_title')
func_5_6_dataset = pd.read_csv('funciones_5_6_dataset.csv')
cast_dataset = pd.read_csv('cast_credits.csv',index_col='lowercase_name') 
crew_dataset = pd.read_csv('crew_credits.csv',index_col='lowercase_name')
modelo_dataset = pd.read_csv('modelo_database.csv')

# Clases para la funcion get_director
class Exito_Individual(BaseModel):
    nombre: str | None = None
    fecha_lanzamiento: str | None = None
    retorno: float | None = None
    costo: float | None = None
    ganancia: float | None = None

class Resumen(BaseModel):
    director: str | None = None
    total_peliculas: int | None = None
    retorno_total: float | None = None
    retorno_promedio: float | None = None
    peliculas: list[Exito_Individual] | None = None

@app.get("/")
async def root():
    """
Returns a welcome message for the root endpoint of the application.

This asynchronous function handles GET requests to the root URL and returns a JSON response containing a message about the project and the author.

Returns:
    dict: A dictionary containing the welcome message.
"""

    return {"mensaje": "Proyecto Individual 1 DataScience, Samuel Rangel DataPT11"}

@app.get("/cantidad_filmaciones_mes/")
async def cantidad_filmaciones_mes(mes: str = ''):

    
    # En el dataset todos los meses inician con mayuscula, por ello se usa .capitalize(), para garantizar el match.
    if mes.capitalize() not in {'Enero','Febrero', 'Marzo','Abril','Mayo', 'Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'}:
        return 'Por favor ingrese un mes valido en español'
    
    # Se extrae un dataframe mas pequeño donde los meses son igual al input, y se cuenta el numero de filas
    total = func_1_4_dataset['month_name'][func_1_4_dataset['month_name']== mes.capitalize()].count()
    return f'{total} películas fueron estrenadas en el mes de {mes.lower()}'

@app.get("/cantidad_filmaciones_dia/")
async def cantidad_filmaciones_dia(dia: str = ''):
    """
Counts the number of films released on a specified day of the week.

This asynchronous function processes a day input, normalizing it for proper matching against a dataset of film releases. It returns the total count of films released on that day, ensuring the input is valid and formatted correctly.

Args:
    dia (str): The day of the week in Spanish for which to count film releases. Defaults to an empty string.

Returns:
    str: A message indicating the number of films released on the specified day, or an error message if the input is invalid.
    """
    # Se acepta los inputs aun si no tienen acentos correctamente.
    if dia.lower() == 'miercoles':
        dia = 'miércoles'
    elif dia.lower() == 'sabado':
        dia = 'sábado'
    # En el dataset los dias de la semana inician con mayuscula, por ello se usa .capitalize(), para garantizar el match.
    if dia.capitalize() not in {'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'}:
        return 'Por favor ingrese un dia de la semana valido en español'
    
    # Se extrae un dataframe mas pequeño donde los dias son igual al input, y se cuenta el numero de filas    
    total = func_1_4_dataset['day_name'][func_1_4_dataset['day_name']== dia.capitalize()].count()
    return f'{total} películas fueron estrenadas en los días {dia.lower()}'

@app.get("/score_titulo/")
async def score_titulo(titulo_de_la_filmacion: str = ''):

    # Para buscar la pelicula, al abrir el dataset, se coloca la columna de titulo como indice, para facilitar la busqueda.
    indice = titulo_de_la_filmacion.lower()

    if indice not in func_1_4_dataset.index:
       return 'Hay algun error en el nombre introducido (considere mayúsculas) o la película no se encuentra en la base de datos'
    
    return f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]} con un score/popularidad de {func_1_4_dataset['popularity'][indice]}"
    
@app.get("/votos_titulo/")
async def votos_titulo(titulo_de_la_filmacion: str = ''):
    """
Retrieves voting information for a specified film title.

This asynchronous function checks the provided film title against a dataset and returns relevant voting details, including the number of votes and the release year. If the film has fewer than 2000 votes, a specific message is returned; otherwise, detailed voting information is provided.

Args:
    titulo_de_la_filmacion (str): The title of the film for which to retrieve voting information. Defaults to an empty string.

Returns:
    str: A message containing the voting information for the specified film or an error message if the title is invalid or not found.
"""


    # Para buscar la pelicula, al abrir el dataset, se coloca la columna de titulo como indice, para facilitar la busqueda.
    indice = titulo_de_la_filmacion.lower()

    if indice not in func_1_4_dataset.index:
       return 'Hay algun error en el nombre introducido (considere mayúsculas) o la película no se encuentra en la base de datos'
    
    return f"La película {func_1_4_dataset['title'][indice]} tiene menos de 2000 valoraciones, por lo que no se devuelve ningun valor." if func_1_4_dataset['vote_count'][indice] < 2000 else f"La película {func_1_4_dataset['title'][indice]} fue estrenada en el año {func_1_4_dataset['release_year'][indice]}. La misma cuenta con un total de {int(func_1_4_dataset['vote_count'][indice])} valoraciones, con un promedio de {func_1_4_dataset['vote_average'][indice]}"

@app.get("/get_actor/")
async def get_actor(nombre_actor: str = ''):
    """
Retrieves film participation and financial return information for a specified actor.

This asynchronous function checks the provided actor's name against a dataset and returns the number of films they have participated in, along with the total financial return and average return per film. If the actor is not found in the dataset, an error message is returned.

Args:
    nombre_actor (str): The name of the actor for whom to retrieve film and return information. Defaults to an empty string.

Returns:
    str: A message containing the actor's film participation details and financial return, or an error message if the actor is not found.
"""
    
    # Se convierte a minuscula para evitar errores, y usar como indice en el cast_dataset
    indice = nombre_actor.lower()

    # se chequea si el actor aparece como indice en el dataset, de no ser asi regresa el mensaje de error
    if indice not in cast_dataset.index:
       return 'Hay algun error en el nombre introducido o el actor no esta en la base de datos'
    
    # Si el actor esta en el dataset, se obtienen las peliculas en cast_dataset, y luego se compara con
    # el dataset de movies (func_5_6_dataset) y nos quedamos solo con aquellos donde el id de la pelicula
    # aparezca en ambas
    movies_cast_id_match = func_5_6_dataset['id'].isin(cast_dataset['id'][indice])
    
    # valores a extraer de ambos datasets para el resultado de la funcion
    nombre = cast_dataset['name'][indice][0]
    filmaciones = func_5_6_dataset['id'][movies_cast_id_match].shape[0]
    retorno = func_5_6_dataset['return'][movies_cast_id_match].sum()
    promedio = retorno/filmaciones

    return f"El actor {nombre} ha participado en {filmaciones} filmaciones, el mismo ha conseguido un retorno de {round(retorno,ndigits=2)} con un promedio de {round(promedio, ndigits=2)} por filmacion."

@app.get("/get_director/")
async def get_director(nombre_director: str = ''):

    # Se convierte a minuscula para evitar errores, y usar como indice en el crew_dataset
    indice = nombre_director.lower()

    # se chequea si el actor aparece como indice en el dataset, de no ser asi regresa el mensaje de error
    if indice not in crew_dataset.index:
       return 'Hay algun error en el nombre introducido o el director no esta en la base de datos'
    
    # Si el director esta en el dataset, se obtienen las peliculas en crew_dataset, y luego se compara con
    # el dataset de movies (func_5_6_dataset) y nos quedamos solo con aquellos donde el id de la pelicula
    # aparezca en ambas
    movies_crew_id_match = func_5_6_dataset['id'].isin(crew_dataset['id'][indice])

    # valores a extraer de ambos datasets para el resultado de la funcion
    filmaciones = func_5_6_dataset['id'][movies_crew_id_match]
    retorno = func_5_6_dataset['return'][movies_crew_id_match].sum()

    # substituyendo los valores en objeto Resumen()
    resumen = Resumen()
    resumen.director = crew_dataset['name'][indice][0]
    resumen.retorno_total = retorno
    resumen.retorno_promedio = retorno/filmaciones.shape[0]

    # lista vacia que sera llenada
    lista_filmaciones = []

    # df que permitira buscar y añadir la info de cada pelicula individual facilmente
    director_films = pd.read_csv('funciones_5_6_dataset.csv', index_col='id')
    for filmacion in filmaciones:
        film = Exito_Individual()
        film.nombre = director_films['title'][filmacion]
        film.fecha_lanzamiento = director_films['release_date'][filmacion]
        film.retorno = director_films['revenue'][filmacion]
        film.costo = director_films['budget'][filmacion]
        film.ganancia = director_films['return'][filmacion]

        lista_filmaciones.append(film)
    
    resumen.peliculas = lista_filmaciones
    resumen.total_peliculas = len(lista_filmaciones)

    return {'resumen': resumen}

@app.get("/recomendacion/")
async def recomendacion(titulo: str = ''):

    # Se chequea que la pelicula esta en el dataset, de no ser asi regresa mensaje de error
    if titulo not in modelo_dataset['title'].tolist():
        return 'Hay algun error en el nombre introducido (considere mayúsculas) o la película no se encuentra en la base de datos'
    
    # instanciar el vectorizador para fijar los parametros, en este caso limite de atributos (palabras) y remover palabras no relevantes
    cv = CountVectorizer(max_features=1250, stop_words='english')

    # la transformacion hace que tengamos tantas columnas como palabras diferentes y ver cuales aparecen
    # aqui la cantidad de palabras diferentes son 1250 pq fue el limite puesto al vectorizador
    vector = cv.fit_transform(modelo_dataset['tags']).toarray()

    # la funcion calcula la semejanza entre cada registro con el resto de los registros
    similitud = cosine_similarity(vector)

    # se busca el indice correspondiente a la pelicula que se ingreso
    indice = modelo_dataset[modelo_dataset['title']== titulo].index[0]

    # con el indice se extrae la fila de la pelicula y toda su semejanza con el resto de peliculas, ordenando de mayor a menor
    distancia = sorted(list(enumerate(similitud[indice])), reverse=True, key=lambda x: x[1])

    """
Extracts specific values from a list, starting from the second to the sixth element.

This function processes a list of values, omitting the first element, which is assumed to be a movie title. It retrieves and returns the specified range of values for further use.

Args:
    values (list): A list containing movie-related data, where the first element is the movie title.

Returns:
    list: A list containing the extracted values from the second to the sixth position.
"""

    return [modelo_dataset['title'][i[0]] for i in distancia[1:6]]
