#Python
from typing import Optional

#Pydantic -> Modelos
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI 
from fastapi import Body, Query

# inicializando app como un objeto de FastAPI
app = FastAPI()

# definiendo el modelo

class Person(BaseModel):
    first_name: str
    last_name: str
    age: str
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None 

@app.get("/")
def home():
    return {"Hello":"World"}

# REQUEST AND RESPONSE BODY

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# VALIDACIONES: Query Parameters
@app.get("/person/detail")
def show_person(
    # atributo: Opcional-u-Obligatorio[tipo] = Query(valorDefault, restricciones)
    name: Optional[str] = Query(None, min_lenght = 1, max_length=50),
    age: str = Query(...)
):
    return {name: age} # Que regresa
# Mas validaciones:
#  Numeros:
#       ge >=
#       le <=
#       gt >
#       lt <
#  Strings:
#       max_lenght
#       min_lenght
#       regex
#  Para documentar mejor:
#       Title
#       Description



