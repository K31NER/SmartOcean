import os
import string
from models import Reporte
from dotenv import load_dotenv
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig

load_dotenv()

# Constanste de configuracion
Email = os.getenv("CORREO")
Codigo = os.getenv("CODIGO")

# Configuración de FastAPI-Mail
conf = ConnectionConfig(
    MAIL_USERNAME=Email,
    MAIL_PASSWORD=Codigo,
    MAIL_FROM=Email,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Estilos css para mas personalizacion
ESTILOS_REPORTE = {
    "Contaminación": {
        "border_color": "#D69E2E", 
        "header_color": "#B7791F", 
    },
    "Emergencia": {
        "border_color": "#E53E3E",  
        "header_color": "#C53030",  
    },
    "Incidente": {
        "border_color": "#3182CE",  
        "header_color": "#2B6CB0",  
    },
    "Otro": {
        "border_color": "#eea511",  
        "header_color": "#e59c08", 
    }
}

async def enviar_correo(data:Reporte,destinario:str):
    
    """ Enviar mensaje de email a los usuarios"""
    
    with open("templates/email.html","r",encoding="utf-8") as file:
        html_template = file.read()
    
    # Validamos el tipo de reporte
    tipo_reporte = data.tipo
    estilos = ESTILOS_REPORTE.get(tipo_reporte, ESTILOS_REPORTE["Otro"])
    
    template = string.Template(html_template)
    html_content = template.safe_substitute(
    lugar=data.lugar ,
    tipo=data.tipo,
    descripcion=data.descripcion,
    nombre=data.nombre or "Anonimo",
    contacto=data.contacto or "Anonimo",
    fecha_creacion=data.fecha_creacion,
    
    # inyectamos el css
    border_color=estilos["border_color"],
    header_color=estilos["header_color"]
)
    
    mensaje = MessageSchema(
        subject="Nuevo reporte",
        recipients=[destinario],
        body=html_content,
        subtype="html"
    )
    
    fm = FastMail(config=conf)
    await fm.send_message(mensaje)