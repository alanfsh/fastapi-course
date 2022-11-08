from fastapi import FastAPI 

# inicializando app como un objeto de FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"Hello":"World"}

# Para iniciar la app desde uvicorn ejecutar:
#   uvicorn main:app --reload
#   uvicorn nombredearchivo:objetoquecontienelaapp --reload

# Documentacion interactiva de OPENAPI
# REDOC Y SWAGER
# se accede desde el navegador en la misma direccion montada

# PATH OPERATIONS
# @app.get("/") # QUE SE ESTA INVOCANDO DESDE EL PATH 127.0.0.1:8080/
# def home(): # QUE SE EJECUTA
#     return {"Hello":"World"} # QUE DEVUELVE

# PATH PARAMETERS --> Parametros obligatorios
# SI ACCEDO A UN PATH COMO /tweets/{tweet_id} --> esto para usar variables e identificar un tweet

# QUERY PARAMETERS --> Parametros opcionales
# /tweets/{tweet_id}/details?age=20&?height=185 los opcionales van con ?

# REQUEST BODY --> Cuando el cliente(navegador) solicita al servidor
# RESPONSE BODY --> Cuando el servidor responde al cliente y envia el JSON