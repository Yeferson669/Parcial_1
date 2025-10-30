from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlmodel import Session
from app.db import get_session
from app import crud, schemas

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=schemas.EmpleadoOut, status_code=status.HTTP_201_CREATED)
def crear_empleado(empleado: schemas.EmpleadoCreate, session: Session = Depends(get_session)):
    return crud.crear_empleado(session, empleado)

@router.get("/", response_model=List[schemas.EmpleadoOut])
def listar_empleados(especialidad: Optional[str] = None, estado: Optional[str] = None, session: Session = Depends(get_session)):
    return crud.listar_empleados(session, especialidad, estado)

@router.get("/{empleado_id}", response_model=schemas.EmpleadoOutFull)
def obtener_empleado(empleado_id: int, session: Session = Depends(get_session)):
    return crud.obtener_empleado(session, empleado_id)

@router.put("/{empleado_id}", response_model=schemas.EmpleadoOut)
def actualizar_empleado(empleado_id: int, empleado: schemas.EmpleadoUpdate, session: Session = Depends(get_session)):
    return crud.actualizar_empleado(session, empleado_id, empleado)

@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(empleado_id: int, session: Session = Depends(get_session)):
    crud.eliminar_empleado(session, empleado_id)
    return None

@router.get("/{empleado_id}/proyectos", response_model=List[schemas.ProyectoOut])
def proyectos_por_empleado(empleado_id: int, session: Session = Depends(get_session)):
    return crud.proyectos_de_empleado(session, empleado_id)
