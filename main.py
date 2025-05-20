from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import create_tables
from router import reporte,render

app = FastAPI(
    title="Reporte de playas",
    lifespan=create_tables
)

templates = Jinja2Templates("templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(reporte.router)
app.include_router(render.router)