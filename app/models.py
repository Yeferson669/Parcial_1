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

    # Relación 1:N → Un empleado puede ser gerente de varios proyectos
    proyectos_gerente = relationship(
        "Proyecto",
        back_populates="gerente",
        cascade="all, delete-orphan"
    )

    # Relación N:M → Empleado puede estar en varios proyectos
    asignaciones = relationship(
        "Asignacion",
        back_populates="empleado",
        cascade="all, delete"
    )

    proyectos = relationship(
        "Proyecto",
        secondary="asignaciones",
        back_populates="empleados"
    )


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    presupuesto = Column(Float)
    estado = Column(String(30))
    gerente_id = Column(Integer, ForeignKey("empleados.id", ondelete="SET NULL"))

    # Relación inversa del gerente
    gerente = relationship("Empleado", back_populates="proyectos_gerente")

    # Relación N:M → Proyecto con varios empleados
    asignaciones = relationship(
        "Asignacion",
        back_populates="proyecto",
        cascade="all, delete"
    )

    empleados = relationship(
        "Empleado",
        secondary="asignaciones",
        back_populates="proyectos"
    )


class Asignacion(Base):
    __tablename__ = "asignaciones"

    empleado_id = Column(Integer, ForeignKey("empleados.id", ondelete="CASCADE"), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), primary_key=True)
    rol = Column(String(100))

    empleado = relationship("Empleado", back_populates="asignaciones")
    proyecto = relationship("Proyecto", back_populates="asignaciones")
