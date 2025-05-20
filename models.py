from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel,Field

class Reporte(SQLModel,table=True):
    id:int = Field(default=None , primary_key=True)
    lugar:str = Field(index=True)
    tipo:str = Field()
    descripcion:str = Field()
    nombre: Optional[str] = Field(default=None,nullable=True)
    contacto:Optional[str] = Field(default=None,nullable=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True