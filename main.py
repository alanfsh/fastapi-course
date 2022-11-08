#Python
from typing import Optional

#Pydantic -> Modelos
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI 
from fastapi import Body

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

