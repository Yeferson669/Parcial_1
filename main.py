from fastapi import FastAPI
from .db import Base, engine
from .routers import empleados, proyectos

app = FastAPI(title="Sistema de Gestión de Proyectos", version="1.0")