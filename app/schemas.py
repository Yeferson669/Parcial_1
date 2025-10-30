from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List


class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    especialidad: str = Field(..., min_length=1)
    salario: float = Field(..., ge=0)
    estado: Optional[str] = Field(default="ACTIVO")


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    especialidad: Optional[str] = None
    salario: Optional[float] = None
    estado: Optional[str] = None


class EmpleadoOut(EmpleadoBase):
    id: int

    class Config:
        orm_mode = True


class AsignacionIn(BaseModel):
    empleado_id: int
    rol: Optional[str] = Field(default=None)


class AsignacionOut(BaseModel):
    empleado_id: int
    proyecto_id: int
    rol: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True


class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: Optional[str] = Field(default=None)
    presupuesto: float = Field(..., ge=0)
    estado: Optional[str] = Field(default="PLANEADO")
    gerente_id: Optional[int] = None


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    presupuesto: Optional[float] = None
    estado: Optional[str] = None
    gerente_id: Optional[int] = None


class ProyectoOut(ProyectoBase):
    id: int
    gerente: Optional[EmpleadoOut] = None
    empleados: List[EmpleadoOut] = []

    class Config:
        orm_mode = True


class EmpleadoOutFull(EmpleadoOut):
    proyectos: List[ProyectoOut] = []

    class Config:
        orm_mode = True


class ProyectoOutFull(ProyectoOut):
    empleados: List[EmpleadoOut] = []
    gerente: Optional[EmpleadoOut] = None

    class Config:
        orm_mode = True



EmpleadoOutFull.update_forward_refs()
ProyectoOut.update_forward_refs()
ProyectoOutFull.update_forward_refs()
