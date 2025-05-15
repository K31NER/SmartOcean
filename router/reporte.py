from fastapi import APIRouter,Depends,Form,Request
from fastapi.responses import RedirectResponse
from db import *
from models import Reporte


router = APIRouter()

@router.post("/report")
def hacer_reporte(session:sesion,lugar:str = Form(...),
                tipo:str=Form(...),descripcion:str = Form(...),
                nombre:str= Form(...),contacto:str = Form(...)):
    # Crear reporte
    new_report = Reporte(
        lugar = lugar,
        tipo = tipo,
        descripcion = descripcion,
        nombre = nombre,
        contacto = contacto
    )
    
    print(new_report)
    #Agreagamos el reporte
    session.add(new_report)
    session.commit()
    session.refresh(new_report)
    
    # Redirigimos al inicio
    response = RedirectResponse(url="/",status_code=303)
    return response