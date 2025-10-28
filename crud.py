from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from . import models, schemas

# ---------- Empleados ----------
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
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp