from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=schemas.ProyectoOut, status_code=status.HTTP_201_CREATED, summary="Crear proyecto con gerente")
def crear_proyecto(proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    return crud.crear_proyecto(db, proyecto)

@router.get("/", response_model=List[schemas.ProyectoOut], summary="Listar proyectos (filtros)")
def listar_proyectos(estado: str = None, presupuesto_min: float = None, presupuesto_max: float = None, db: Session = Depends(get_db)):
    return crud.listar_proyectos(db, estado, presupuesto_min, presupuesto_max)

