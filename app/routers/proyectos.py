from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=schemas.ProyectoOut, status_code=status.HTTP_201_CREATED, summary="Crear proyecto con gerente")
def crear_proyecto(proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    return crud.crear_proyecto(db, proyecto)

@router.get("/", response_model=List[schemas.ProyectoOut], summary="Listar proyectos (filtros)")
def listar_proyectos(estado: str = None, presupuesto_min: float = None, presupuesto_max: float = None, db: Session = Depends(get_db)):
    return crud.listar_proyectos(db, estado, presupuesto_min, presupuesto_max)

@router.get("/{proyecto_id}", response_model=schemas.ProyectoOut, summary="Obtener proyecto, gerente y empleados")
def get_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return crud.obtener_proyecto(db, proyecto_id)

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar proyecto")
def delete_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    crud.eliminar_proyecto(db, proyecto_id)
    return None

@router.post("/{proyecto_id}/asignaciones", status_code=status.HTTP_201_CREATED, summary="Asignar empleado a proyecto")
def asignar(proyecto_id: int, asign_in: schemas.AsignacionIn, db: Session = Depends(get_db)):
    return crud.asignar_empleado(db, proyecto_id, asign_in)

@router.delete("/{proyecto_id}/asignaciones/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desasignar empleado")
def desasignar(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    crud.desasignar_empleado(db, proyecto_id, empleado_id)
    return None

@router.get("/{proyecto_id}/empleados", response_model=List[schemas.EmpleadoOut], summary="Empleados de un proyecto")
def empleados_del_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return crud.empleados_de_proyecto(db, proyecto_id)

@router.get("/por_empleado/{empleado_id}", response_model=List[schemas.ProyectoOut], summary="Proyectos de un empleado")
def proyectos_por_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return crud.proyectos_de_empleado(db, empleado_id)