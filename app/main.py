from fastapi import FastAPI
from app.db import Base, engine
from app.routers import empleados, proyectos

app = FastAPI(title="Sistema de Gestión de Proyectos", version="1.0")
Base.metadata.create_all(bind=engine)

app.include_router(empleados.router)
app.include_router(proyectos.router)

