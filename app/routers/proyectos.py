from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


# Crear proyecto con gerente
@router.post(
    "/", 
    response_model=schemas.ProyectoOut, 
    status_code=status.HTTP_201_CREATED, 
    summary="Crear proyecto con gerente"
)
def crear_proyecto(proyecto_in: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    return crud.crear_proyecto(db, proyecto_in)


# Listar proyectos con filtros
@router.get(
    "/", 
    response_model=List[schemas.ProyectoOut], 
    summary="Listar proyectos (filtro: estado, presupuesto)"
)
def listar_proyectos(
    estado: Optional[str] = None,
    presupuesto_min: Optional[float] = None,
    presupuesto_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return crud.listar_proyectos(db, estado, presupuesto_min, presupuesto_max)


# Obtener proyecto, su gerente y sus empleados
@router.get(
    "/{proyecto_id}", 
    response_model=schemas.ProyectoOut, 
    summary="Obtener proyecto, su gerente y sus empleados"
)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return crud.obtener_proyecto(db, proyecto_id)


# Eliminar proyecto (cascada)
@router.delete(
    "/{proyecto_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Eliminar proyecto (en cascada)"
)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    crud.eliminar_proyecto(db, proyecto_id)
    return None


# Asignar empleado a proyecto
@router.post(
    "/{proyecto_id}/asignaciones", 
    summary="Asignar empleado a proyecto"
)
def asignar_empleado(proyecto_id: int, asign_in: schemas.AsignacionIn, db: Session = Depends(get_db)):
    return crud.asignar_empleado(db, proyecto_id, asign_in)


# Desasignar empleado de proyecto
@router.delete(
    "/{proyecto_id}/asignaciones/{empleado_id}", 
    summary="Desasignar empleado de proyecto"
)
def desasignar_empleado(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    return crud.desasignar_empleado(db, proyecto_id, empleado_id)

