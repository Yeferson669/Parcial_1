from pydantic import BaseModel, Field
from typing import Optional, List

class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    especialidad: str = Field(..., min_length=1)
    salario: float = Field(..., ge=0)
    estado: Optional[str] = Field("ACTIVO")

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str]
    especialidad: Optional[str]
    salario: Optional[float]
    estado: Optional[str]

class EmpleadoOut(EmpleadoBase):
    id: int
    class Config:
        orm_mode = True

class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    presupuesto: float = Field(..., ge=0)
    estado: Optional[str] = Field("PLANEADO")
    gerente_id: Optional[int] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    presupuesto: Optional[float]
    estado: Optional[str]
    gerente_id: Optional[int]