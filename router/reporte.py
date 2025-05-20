import os
from db import *
from models import Reporte
from sqlmodel import select
from datetime import datetime
from dotenv import load_dotenv
from utils import enviar_correo
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Depends,Form,Request

load_dotenv()

correo = os.getenv("DESTINARIO")

router = APIRouter()

@router.post("/report",description="Generar nuevos reportes y enviar correo")
async def hacer_reporte(session:sesion,lugar:str = Form(...),
                tipo:str=Form(...),descripcion:str = Form(...),
                nombre:str= Form(...),contacto:str = Form(...)):
    
    # Sacamos la fecha
    fecha_str = datetime.now().strftime("%d/%m/%Y, %H")
    fecha_actual = datetime.strptime(fecha_str, "%d/%m/%Y, %H")
    
    # Crear reporte
    new_report = Reporte(
        lugar = lugar,
        tipo = tipo,
        descripcion = descripcion,
        nombre = nombre,
        contacto = contacto,
        fecha_creacion=fecha_actual
    )
    
    #Agreagamos el reporte
    session.add(new_report)
    session.commit()
    session.refresh(new_report)
    
    # Enviar correo
    await enviar_correo(data=new_report,destinario=correo)
    
    # Redirigimos al inicio
    response = RedirectResponse(url="/",status_code=303)
    return response

@router.get("/listar_informes",description="Listar los reportes existentes")
async def listar_reportes(session:sesion):
    reportes = session.exec(select(Reporte)).all()
    
    reportes_formateados = []
    
    # Formateamos la fecha
    for reporte in reportes:
        reporte_dict = reporte.dict()
        reporte_dict["fecha_creacion"] = reporte.fecha_creacion.strftime("%d/%m/%Y, %H")
        reportes_formateados.append(reporte_dict)
    
    return reportes_formateados