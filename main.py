#Python
from typing import Optional
from enum import Enum

#Pydantic -> Modelos
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


#FastAPI
from fastapi import FastAPI 
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class PersonBase(BaseModel):
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
    
class Person(PersonBase):
    password: str = Field(..., min_length=8, example="estaesmipass")

class PersonOut(PersonBase):
    pass    

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="juanl97")
    message: str = Field(default="Login Successfully")
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
       

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello":"World"}

# REQUEST AND RESPONSE BODY

@app.post(
    path="/person/new",
    response_model=PersonOut, # Se devuelve el MODELO sin contraseña
    status_code=status.HTTP_201_CREATED) # se devuelve un status code personalizado
def create_person(person: Person = Body(...)):
    return person

# VALIDACIONES: Query Parameters
@app.get(
    path="/person/detail",
    )
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
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
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
@app.put(
    path="/person/{person_id}",
    response_model=PersonOut,
    status_code=status.HTTP_202_ACCEPTED)
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

# Status Code 
# 100 Information
# 200 OK
#   201 Created
#   204 Not Content
# 300 Redirecting
# 400 Client Error
#   404 Not found
#   422 Validation Error
# 500 Internal Server Error
# Se agregan como argumento en cada DECORADOR para especificar que respuesta debe dar al ejecutarse

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# COOKIES AND HEADERS PARAMETERS
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# TIPOS DE ENTRADAS DE DATOS
#   PATH PARAMETERS --> PARAMETROS OBLIGATORIOS EN URL
#   QUERY PARAMETERS --> PARAMETROS OPCIONALES EN URL
#   REQUEST BODY --> JSON ENVIADO POR EL CLIENTE
#   FORMS --> FORMULAROS ENVIADOS POR EL CLIENTE
#   HEADERS --> CABECERAS ENVIADAS
#   COOKIES --> DATOS DE SEGUIMIENTO
#   FILES --> PARA SUBIR ARCHIVOS DESDE EL CLIENTE

# FILES
#   FILE
#   UPLOAD FILE
#       FILENAME
#       CONTENT_FILE (TIPO DE ARCHIVO)
#       FILE(ACCEDER AL ARCHIVO)

# FILES

@app.post(
    path="/post-image",
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024, ndigits=2)
    }