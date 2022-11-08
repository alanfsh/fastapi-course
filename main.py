#Python
from typing import Optional

#Pydantic -> Modelos
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI 
from fastapi import Body, Query, Path

# inicializando app como un objeto de FastAPI
app = FastAPI()

# definiendo el modelo
class Location(BaseModel):
    city: str
    state: str
    country: str

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
    name: Optional[str] = Query(
        None,
        min_lenght = 1, 
        max_length=50,
        title = "Person Name",
        description= "This is the person name. It's between 1 and 50 characters"  
        ),
    age: str = Query(
        ...,
        title = "Person Age",
        description= "This is the person age. It's required"  
        )
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

# Validaciones PATH PARAMETERS
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0, # GREATER THAN 0
        title = "Person ID",
        description= "This is the person id. It's required",
        )
):
    return {person_id: "It exists"}

# Validaciones REQUEST BODY
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict)
    
    return person
