from fastapi import FastAPI
from db import create_tables
from router import reporte,render
from utils.clima import update_weather
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_crons import Crons,get_cron_router

app = FastAPI(
    title="Reporte de playas",
    lifespan=create_tables,
    docs_url=None, redoc_url=None
)
crons = Crons(app)

# Añadimos el router de crons a la aplicación
app.include_router(get_cron_router(), prefix="/api",tags=["Tareas"])

# Creamos una tarea programada que se ejecutarla en las horas definidas
@crons.cron("0 6,12,20 * * *", name="Update Popularidad")
async def check_popularidad():
    print("⚡ Actualizando el clima de las playas...")
    try:
        update_weather()
        return {"Status": "Json actualizado con exito"}
    except Exception as e:
        return {"status": f"error al actualizar {e}"}
    
templates = Jinja2Templates("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(reporte.router)
app.include_router(render.router)