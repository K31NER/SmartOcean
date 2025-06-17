import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends,FastAPI
from utils.clima import update_weather
from sqlmodel import create_engine,SQLModel,Session

load_dotenv()

URL = os.getenv("DB_URL")

engine = create_engine(URL)

def get_session():
    """ Crear conexion con la base de datos """
    with Session(engine) as session:
        yield session

def startup(app:FastAPI):
    """ Inicializa la base de datos y la actualizacion de los climas al iniciar el servidor"""
    
    # Creamos todas las tablas
    print("Tablas creadas ✅")
    SQLModel.metadata.create_all(engine)
    
    # Actualizamos los datos climaticos
    print("Datos climaticos actualizados 🌐")
    update_weather()
    yield
    
# Generar dependencia de sessiom 
sesion = Annotated[Session,Depends(get_session)]
        