from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    estado = Column(String, default="ACTIVO")

    proyectos = relationship("Asignacion", back_populates="empleado", cascade="all, delete-orphan")
    proyectos_dirige = relationship("Proyecto", back_populates="gerente")


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String)
    presupuesto = Column(Float, nullable=False)
    estado = Column(String, default="PLANEADO")
    gerente_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)

    gerente = relationship("Empleado", back_populates="proyectos_dirige")
    empleados = relationship("Asignacion", back_populates="proyecto", cascade="all, delete-orphan")


class Asignacion(Base):
    __tablename__ = "asignaciones"

    empleado_id = Column(Integer, ForeignKey("empleados.id"), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), primary_key=True)
    rol = Column(String)

    empleado = relationship("Empleado", back_populates="proyectos")
    proyecto = relationship("Proyecto", back_populates="empleados")
