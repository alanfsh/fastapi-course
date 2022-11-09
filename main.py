#Python
from typing import Optional
from enum import Enum

#Pydantic -> Modelos
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


#FastAPI
from fastapi import FastAPI 
from fastapi import Body, Query, Path

# inicializando app como un objeto de FastAPI
app = FastAPI()

# definiendo el modelo
class HairColor(Enum): #Definiendo los colores aceptados
    white = "white"
    brown = "brown"
    black = "black"
    blonce = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="monterrey"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="nuevo leon"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="mexico"
    )

class Person(BaseModel):
    # con Field validamos los Modelos
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Juan"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Perez Montes"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=33
    )
    email: EmailStr = Field(
        ...,
        example="juan_montes@gmail.com"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="white")
    is_married: Optional[bool] = Field(default=None, example="false")
    password: str = Field(..., min_length=8)
    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "first_name": "Juan",
    #             "last_name": "Perez Montes",
    #             "age": 32,
    #             "email": "juanpmont@gmail.com",
    #             "hair_color": "black",
    #             "is_married": "True"
    #         }
    #     }

class PersonOut(BaseModel):
    # con Field validamos los Modelos
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Juan"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Perez Montes"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=33
    )
    email: EmailStr = Field(
        ...,
        example="juan_montes@gmail.com"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="white")
    is_married: Optional[bool] = Field(default=None, example="false")

    # Tipos de datos
      # Clasicos
        # str
        # int
        # float
        # bool
      
      # Especiales --> se importan de pydantic
        # Enum
        # HttpUrl --> valida que sea un link
        # FilePath --> Valida la direccion a un archivo
        # DirectoryPath --> Valida la direccion a una carpeta
        # EmailStr --> valida que sea un email
        # PaymentCardNumber 
        # IPvAnyAdress
        # NegativeFloat
        # PositiveFloat
        # NegativeInt
        # PositiveInt
       

@app.get("/")
def home():
    return {"Hello":"World"}

# REQUEST AND RESPONSE BODY

@app.post("/person/new", response_model=PersonOut) # Se devuelve el MODELO sin contraseña
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
        description= "This is the person name. It's between 1 and 50 characters",
        example="Jose"  
        ),
    age: int = Query(
        ...,
        title = "Person Age",
        description= "This is the person age. It's required",
        example=25
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
        example=125
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
        gt=0,
        example=132 #Aqui esta el ejemplo para no rellenar al probar
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return person
