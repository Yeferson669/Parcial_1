from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Asignacion(SQLModel, table=True):
    empleado_id: Optional[int] = Field(default=None, foreign_key="empleado.id", primary_key=True)
    proyecto_id: Optional[int] = Field(default=None, foreign_key="proyecto.id", primary_key=True)
    rol: Optional[str] = Field(default=None)


class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    presupuesto: float
    estado: Optional[str] = Field(default="PLANEADO")
    gerente_id: Optional[int] = Field(default=None, foreign_key="empleado.id")

    gerente: Optional["Empleado"] = Relationship(back_populates="proyectos_gerenciados", sa_relationship_kwargs={"lazy": "joined"})
    empleados: List["Empleado"] = Relationship(back_populates="proyectos", link_model=Asignacion)


class Empleado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    salario: float
    estado: Optional[str] = Field(default="ACTIVO")

    proyectos: List[Proyecto] = Relationship(back_populates="empleados", link_model=Asignacion)
    proyectos_gerenciados: List[Proyecto] = Relationship(back_populates="gerente", sa_relationship_kwargs={"lazy": "joined"})
