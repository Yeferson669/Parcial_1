from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=schemas.EmpleadoOut, status_code=status.HTTP_201_CREATED)
def crear_empleado(empleado_in: schemas.EmpleadoCreate, db: Session = Depends(get_db)):
    return crud.crear_empleado(db, empleado_in)

@router.get("/", response_model=List[schemas.EmpleadoOut])
def listar_empleados(especialidad: Optional[str] = None, estado: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.listar_empleados(db, especialidad, estado)

@router.get("/{empleado_id}", response_model=schemas.EmpleadoOut)
def obtener_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return crud.obtener_empleado(db, empleado_id)

@router.put("/{empleado_id}", response_model=schemas.EmpleadoOut)
def actualizar_empleado(empleado_id: int, empleado_in: schemas.EmpleadoUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_empleado(db, empleado_id, empleado_in)

@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(empleado_id: int, db: Session = Depends(get_db)):
    crud.eliminar_empleado(db, empleado_id)
    return None

@router.get("/{empleado_id}/proyectos")
def proyectos_de_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return crud.proyectos_de_empleado(db, empleado_id)
