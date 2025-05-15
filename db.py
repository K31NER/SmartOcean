from sqlmodel import create_engine,SQLModel,Session
from fastapi import Depends,FastAPI
from typing import Annotated

URL = "sqlite:///./report.db"

engine = create_engine(URL, connect_args={"check_same_thread":False})

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
        