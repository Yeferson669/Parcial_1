from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session
from app.db import get_session
from app import crud, schemas

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=schemas.ProyectoOut, status_code=status.HTTP_201_CREATED)
def crear_proyecto(proyecto: schemas.ProyectoCreate, session: Session = Depends(get_session)):
    return crud.crear_proyecto(session, proyecto)

@router.get("/", response_model=List[schemas.ProyectoOut])
def listar_proyectos(
    estado: Optional[str] = Query(None, description="Filtrar por estado del proyecto"),
    presupuesto: Optional[float] = Query(None, description="Filtrar por presupuesto exacto"),
    session: Session = Depends(get_session)
):
    try:
        return crud.listar_proyectos(session=session, estado=estado, presupuesto=presupuesto)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al listar proyectos: {str(e)}")

@router.get("/{proyecto_id}", response_model=schemas.ProyectoOut)
def obtener_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    return crud.obtener_proyecto(session, proyecto_id)

@router.put("/{proyecto_id}", response_model=schemas.ProyectoOut)
def actualizar_proyecto(proyecto_id: int, proyecto: schemas.ProyectoUpdate, session: Session = Depends(get_session)):
    return crud.actualizar_proyecto(session, proyecto_id, proyecto)

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    crud.eliminar_proyecto(session, proyecto_id)
    return None

@router.post("/{proyecto_id}/asignar", status_code=status.HTTP_201_CREATED)
def asignar_empleado(proyecto_id: int, asign_in: schemas.AsignacionIn, session: Session = Depends(get_session)):
    return crud.asignar_empleado(session, proyecto_id, asign_in)

@router.delete("/{proyecto_id}/desasignar/{empleado_id}")
def desasignar_empleado(proyecto_id: int, empleado_id: int, session: Session = Depends(get_session)):
    return crud.desasignar_empleado(session, proyecto_id, empleado_id)

@router.put("/{proyecto_id}/gerente/{empleado_id}")
def asignar_gerente(proyecto_id: int, empleado_id: int, session: Session = Depends(get_session)):
    return crud.asignar_gerente(session, proyecto_id, empleado_id)

@router.get("/{proyecto_id}/empleados", response_model=List[schemas.EmpleadoOut])
def empleados_de_proyecto(proyecto_id: int, session: Session = Depends(get_session)):
    return crud.empleados_de_proyecto(session, proyecto_id)
