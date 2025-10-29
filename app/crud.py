from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def crear_empleado(db: Session, empleado_in: schemas.EmpleadoCreate):
    nuevo = models.Empleado(**empleado_in.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_empleados(db: Session, especialidad: str = None, estado: str = None):
    q = db.query(models.Empleado)
    if especialidad:
        q = q.filter(models.Empleado.especialidad == especialidad)
    if estado:
        q = q.filter(models.Empleado.estado == estado)
    return q.all()

def obtener_empleado(db: Session, empleado_id: int):
    emp = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return emp

def actualizar_empleado(db: Session, empleado_id: int, empleado_in: schemas.EmpleadoUpdate):
    emp = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    for k, v in empleado_in.dict(exclude_unset=True).items():
        setattr(emp, k, v)
    db.commit()
    db.refresh(emp)
    return emp

def eliminar_empleado(db: Session, empleado_id: int):
    emp = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    proyectos_gerente = db.query(models.Proyecto).filter(models.Proyecto.gerente_id == emp.id).all()
    if proyectos_gerente:
        raise HTTPException(status_code=409, detail="Empleado es gerente de uno o más proyectos")
    db.delete(emp)
    db.commit()
    return {"message": "Empleado eliminado correctamente"}

def crear_proyecto(db: Session, proyecto_in: schemas.ProyectoCreate):
    existe = db.query(models.Proyecto).filter(models.Proyecto.nombre == proyecto_in.nombre).first()
    if existe:
        raise HTTPException(status_code=409, detail="Ya existe un proyecto con ese nombre")
    if proyecto_in.gerente_id:
        gerente = db.query(models.Empleado).filter(models.Empleado.id == proyecto_in.gerente_id).first()
        if not gerente:
            raise HTTPException(status_code=404, detail="Gerente no encontrado")
    nuevo = models.Proyecto(**proyecto_in.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_proyectos(db: Session, estado: str = None, presupuesto_min: float = None, presupuesto_max: float = None):
    q = db.query(models.Proyecto)
    if estado:
        q = q.filter(models.Proyecto.estado == estado)
    if presupuesto_min is not None:
        q = q.filter(models.Proyecto.presupuesto >= presupuesto_min)
    if presupuesto_max is not None:
        q = q.filter(models.Proyecto.presupuesto <= presupuesto_max)
    return q.all()

def obtener_proyecto(db: Session, proyecto_id: int):
    p = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return p

def eliminar_proyecto(db: Session, proyecto_id: int):
    p = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(p)
    db.commit()
    return {"message": "Proyecto eliminado correctamente"}

def asignar_empleado(db: Session, proyecto_id: int, asign_in: schemas.AsignacionIn):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = db.query(models.Empleado).filter(models.Empleado.id == asign_in.empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    existe = db.query(models.Asignacion).filter(
        models.Asignacion.empleado_id == asign_in.empleado_id,
        models.Asignacion.proyecto_id == proyecto_id
    ).first()
    if existe:
        raise HTTPException(status_code=409, detail="Empleado ya asignado a este proyecto")
    nueva = models.Asignacion(empleado_id=asign_in.empleado_id, proyecto_id=proyecto_id, rol=asign_in.rol)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"message": "Empleado asignado correctamente"}

def desasignar_empleado(db: Session, proyecto_id: int, empleado_id: int):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    if proyecto.gerente_id == empleado_id:
        proyecto.gerente_id = None
        db.commit()
        return {"message": "Gerente desasignado correctamente"}
    asignacion = db.query(models.Asignacion).filter(
        models.Asignacion.proyecto_id == proyecto_id,
        models.Asignacion.empleado_id == empleado_id
    ).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    db.delete(asignacion)
    db.commit()
    return {"message": "Empleado desasignado correctamente"}

def proyectos_de_empleado(db: Session, empleado_id: int):
    emp = db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    proyectos = db.query(models.Proyecto).join(models.Asignacion).filter(
        models.Asignacion.empleado_id == empleado_id
    ).all()
    proyectos_gerente = db.query(models.Proyecto).filter(models.Proyecto.gerente_id == empleado_id).all()
    return {"empleado": emp, "proyectos": proyectos + proyectos_gerente}

def empleados_de_proyecto(db: Session, proyecto_id: int):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleados = db.query(models.Empleado).join(models.Asignacion).filter(
        models.Asignacion.proyecto_id == proyecto_id
    ).all()
    if proyecto.gerente_id:
        gerente = db.query(models.Empleado).filter(models.Empleado.id == proyecto.gerente_id).first()
        if gerente and gerente not in empleados:
            empleados.append(gerente)
    return {"proyecto": proyecto, "empleados": empleados}
