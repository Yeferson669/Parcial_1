from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, Depends, status
from typing import List, Set, Optional
from app import models, schemas
from app.models import Proyecto
from app.db import get_session

# ---------- EMPLEADOS ----------

def crear_empleado(session: Session, empleado: schemas.EmpleadoCreate):
    # 🔹 Validar duplicado por nombre + especialidad
    empleado_existente = session.exec(
        select(models.Empleado).where(
            (models.Empleado.nombre == empleado.nombre) &
            (models.Empleado.especialidad == empleado.especialidad)
        )
    ).first()

    if empleado_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un empleado con el nombre '{empleado.nombre}' y especialidad '{empleado.especialidad}'."
        )

    nuevo = models.Empleado(**empleado.dict())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def listar_empleados(session: Session, especialidad: str = None, estado: str = None):
    query = select(models.Empleado).options(
        selectinload(models.Empleado.proyectos),
        selectinload(models.Empleado.proyectos_gerenciados)
    )
    if especialidad:
        query = query.where(models.Empleado.especialidad == especialidad)
    if estado:
        query = query.where(models.Empleado.estado == estado)
    return session.exec(query).all()


def obtener_empleado(session: Session, empleado_id: int):
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


def actualizar_empleado(session: Session, empleado_id: int, data: schemas.EmpleadoUpdate):
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(empleado, k, v)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado


def eliminar_empleado(session: Session, empleado_id: int):
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if empleado.proyectos_gerenciados and len(empleado.proyectos_gerenciados) > 0:
        raise HTTPException(status_code=409, detail="Empleado es gerente de proyectos; reasigne antes de eliminar")
    session.delete(empleado)
    session.commit()
    return {"message": "Empleado eliminado correctamente"}


# ---------- PROYECTOS ----------

def crear_proyecto(session: Session, proyecto: schemas.ProyectoCreate):
    existe = session.exec(select(models.Proyecto).where(models.Proyecto.nombre == proyecto.nombre)).first()
    if existe:
        raise HTTPException(status_code=409, detail="Ya existe un proyecto con ese nombre")
    nuevo = models.Proyecto(**proyecto.dict())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


from typing import Optional, List
from sqlmodel import select
from fastapi import Depends, HTTPException
from app.models import Proyecto
from app.db import get_session
from sqlmodel import Session




def listar_proyectos(
    session: Session = Depends(get_session),
    estado: Optional[str] = None,
    presupuesto: Optional[float] = None
) -> List[Proyecto]:
    try:
        query = select(Proyecto)

        if estado:
            query = query.where(Proyecto.estado == estado)

        if presupuesto is not None:
            query = query.where(Proyecto.presupuesto == presupuesto)

        proyectos = session.exec(query).all()

        if not proyectos:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos con esos filtros")

        return proyectos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar proyectos: {str(e)}")





def actualizar_proyecto(session: Session, proyecto_id: int, data: schemas.ProyectoUpdate):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    new_name = data.dict(exclude_unset=True).get("nombre")
    if new_name and new_name != proyecto.nombre:
        existe = session.exec(select(models.Proyecto).where(models.Proyecto.nombre == new_name)).first()
        if existe:
            raise HTTPException(status_code=409, detail="Ya existe un proyecto con ese nombre")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(proyecto, k, v)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


def eliminar_proyecto(session: Session, proyecto_id: int):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    session.delete(proyecto)
    session.commit()
    return {"message": "Proyecto eliminado correctamente"}


# ---------- ASIGNACIONES ----------

def asignar_empleado(session: Session, proyecto_id: int, asign_in: schemas.AsignacionIn):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = session.get(models.Empleado, asign_in.empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    existe = session.exec(
        select(models.Asignacion).where(
            models.Asignacion.proyecto_id == proyecto_id,
            models.Asignacion.empleado_id == asign_in.empleado_id
        )
    ).first()
    if existe:
        raise HTTPException(status_code=409, detail="Empleado ya asignado a este proyecto")

    nueva = models.Asignacion(proyecto_id=proyecto_id, empleado_id=asign_in.empleado_id, rol=asign_in.rol)
    session.add(nueva)
    session.commit()
    return {"message": "Asignación creada correctamente"}


def desasignar_empleado(session: Session, proyecto_id: int, empleado_id: int):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    if proyecto.gerente_id == empleado_id:
        proyecto.gerente_id = None
        session.add(proyecto)
        asignacion = session.exec(
            select(models.Asignacion).where(
                models.Asignacion.proyecto_id == proyecto_id,
                models.Asignacion.empleado_id == empleado_id
            )
        ).first()
        if asignacion:
            session.delete(asignacion)
        session.commit()
        return {"message": "Empleado era gerente; se quitó como gerente y se eliminó asignación si existía"}

    asignacion = session.exec(
        select(models.Asignacion).where(
            models.Asignacion.proyecto_id == proyecto_id,
            models.Asignacion.empleado_id == empleado_id
        )
    ).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    session.delete(asignacion)
    session.commit()
    return {"message": "Asignación eliminada correctamente"}


def asignar_gerente(session: Session, proyecto_id: int, empleado_id: int):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    proyecto.gerente_id = empleado_id
    session.add(proyecto)

    existe_asign = session.exec(
        select(models.Asignacion).where(
            models.Asignacion.proyecto_id == proyecto_id,
            models.Asignacion.empleado_id == empleado_id
        )
    ).first()
    if not existe_asign:
        nueva = models.Asignacion(proyecto_id=proyecto_id, empleado_id=empleado_id, rol="Gerente")
        session.add(nueva)

    session.commit()
    session.refresh(proyecto)
    return {"message": "Gerente asignado/reasignado correctamente"}


def proyectos_de_empleado(session: Session, empleado_id: int):
    empleado = session.get(models.Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    proyectos_asignados = empleado.proyectos or []
    proyectos_dirige = empleado.proyectos_gerenciados or []
    combined: List[models.Proyecto] = []
    seen: Set[int] = set()
    for p in proyectos_asignados + proyectos_dirige:
        if p.id not in seen:
            combined.append(p)
            seen.add(p.id)
    return combined


def empleados_de_proyecto(session: Session, proyecto_id: int):
    proyecto = session.get(models.Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    _ = proyecto.empleados
    return proyecto.empleados


def obtener_proyecto(session: Session, proyecto_id: int):
    from sqlalchemy.orm import selectinload

    proyecto = session.exec(
        select(models.Proyecto)
        .options(
            selectinload(models.Proyecto.gerente),
            selectinload(models.Proyecto.empleados)
        )
        .where(models.Proyecto.id == proyecto_id)
    ).first()

    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    
    return {
        "id": proyecto.id,
        "nombre": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "presupuesto": proyecto.presupuesto,
        "estado": proyecto.estado,
        "gerente": {
            "id": proyecto.gerente.id,
            "nombre": proyecto.gerente.nombre,
            "especialidad": proyecto.gerente.especialidad,
            "salario": proyecto.gerente.salario,
            "estado": proyecto.gerente.estado,
        } if proyecto.gerente else None,
        "empleados": [
            {
                "id": e.id,
                "nombre": e.nombre,
                "especialidad": e.especialidad,
                "salario": e.salario,
                "estado": e.estado,
            } for e in proyecto.empleados
        ]
    }
