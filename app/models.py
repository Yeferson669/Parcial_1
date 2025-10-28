from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from .db import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    salario = Column(Numeric(12, 2))
    estado = Column(String(30))

    proyectos_gerente = relationship("Proyecto", back_populates="gerente")
    asignaciones = relationship("Asignacion", back_populates="empleado", cascade="all, delete")

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    presupuesto = Column(Float)
    estado = Column(String(30))
    gerente_id = Column(Integer, ForeignKey("empleados.id", ondelete="SET NULL"))

    gerente = relationship("Empleado", back_populates="proyectos_gerente")
    asignaciones = relationship("Asignacion", back_populates="proyecto", cascade="all, delete")

class Asignacion(Base):
    __tablename__ = "asignaciones"

    empleado_id = Column(Integer, ForeignKey("empleados.id", ondelete="CASCADE"), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), primary_key=True)
    rol = Column(String(100))

    empleado = relationship("Empleado", back_populates="asignaciones")
    proyecto = relationship("Proyecto", back_populates="asignaciones")
