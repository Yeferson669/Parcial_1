from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=schemas.EmpleadoOut, status_code=status.HTTP_201_CREATED, summary="Crear empleado")
def crear_empleado(empleado: schemas.EmpleadoCreate, db: Session = Depends(get_db)):
    return crud.crear_empleado(db, empleado)

@router.get("/", response_model=List[schemas.EmpleadoOut], summary="Listar empleados (filtros)")
def listar_empleados(especialidad: str = None, estado: str = None, db: Session = Depends(get_db)):
    return crud.listar_empleados(db, especialidad, estado)

@router.get("/{empleado_id}", response_model=schemas.EmpleadoOut, summary="Obtener empleado")
def get_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return crud.obtener_empleado(db, empleado_id)


@router.put("/{empleado_id}", response_model=schemas.EmpleadoOut, summary="Actualizar empleado")
def update_empleado(empleado_id: int, empleado_in: schemas.EmpleadoUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_empleado(db, empleado_id, empleado_in)

@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar empleado")
def delete_empleado(empleado_id: int, db: Session = Depends(get_db)):
    crud.eliminar_empleado(db, empleado_id)
    return None
