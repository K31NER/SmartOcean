from fastapi import FastAPI
from db import create_tables
from router import reporte,render

app = FastAPI(
    title="Reporte de playas",
    lifespan=create_tables
)

app.include_router(reporte.router)
app.include_router(render.router)