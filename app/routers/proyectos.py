from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=schemas.ProyectoOut, status_code=status.HTTP_201_CREATED)
def crear_proyecto(proyecto_in: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    return crud.crear_proyecto(db, proyecto_in)

@router.get("/", response_model=List[schemas.ProyectoOut])
def listar_proyectos(
    estado: Optional[str] = None,
    presupuesto_min: Optional[float] = None,
    presupuesto_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return crud.listar_proyectos(db, estado, presupuesto_min, presupuesto_max)

@router.get("/{proyecto_id}", response_model=schemas.ProyectoOut)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return crud.obtener_proyecto(db, proyecto_id)

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    crud.eliminar_proyecto(db, proyecto_id)
    return None

@router.post("/{proyecto_id}/asignar")
def asignar_empleado(proyecto_id: int, asign_in: schemas.AsignacionIn, db: Session = Depends(get_db)):
    return crud.asignar_empleado(db, proyecto_id, asign_in)

@router.delete("/{proyecto_id}/desasignar/{empleado_id}")
def desasignar_empleado(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    return crud.desasignar_empleado(db, proyecto_id, empleado_id)

@router.get("/{proyecto_id}/empleados")
def empleados_de_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return crud.empleados_de_proyecto(db, proyecto_id)


@router.put("/{proyecto_id}/gerente/{empleado_id}")
def asignar_gerente(proyecto_id: int, empleado_id: int, db: Session = Depends(get_db)):
    return crud.asignar_gerente(db, proyecto_id, empleado_id)
