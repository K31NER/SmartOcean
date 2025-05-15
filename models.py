from sqlmodel import SQLModel,Field

class Reporte(SQLModel,table=True):
    id:int = Field(default=None , primary_key=True)
    lugar:str = Field(index=True)
    tipo:str = Field()
    descripcion:str = Field()
    nombre:str = Field()
    contacto:str = Field()
    
    class Config:
        orm_mode = True