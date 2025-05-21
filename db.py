from sqlmodel import create_engine,SQLModel,Session
from fastapi import Depends,FastAPI
from dotenv import load_dotenv
from typing import Annotated
import os

load_dotenv()

URL = os.getenv("DB_URL")

engine = create_engine(URL, echo=True)

def get_session():
    """ Crear conexion con la base de datos """
    with Session(engine) as session:
        yield session

def create_tables(app:FastAPI):
    """ Crear todas las tablas de la base de datos"""
    SQLModel.metadata.create_all(engine)
    yield
   
# Generar dependencia de sessiom 
sesion = Annotated[Session,Depends(get_session)]
        