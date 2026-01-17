from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    cedula = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    negocio = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    prestamos = relationship('Prestamo', back_populates='cliente')
    recordatorios = relationship("Recordatorio", back_populates="cliente", cascade="all, delete-orphan")

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    monto = Column(Float)
    fecha = Column(Date)
    estado = Column(String, nullable=False, default='activo')
    cliente = relationship('Cliente', back_populates='prestamos')
    pagos = relationship('Pago', back_populates='prestamo')

class Pago(Base):
    __tablename__ = 'pagos'
    id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey('prestamos.id'))
    monto = Column(Float)
    fecha = Column(Date)
    motivo_no_pago = Column(String, nullable=True)  # Nuevo campo para motivo de no abono
    prestamo = relationship('Prestamo', back_populates='pagos')


class Gasto(Base):
    __tablename__ = 'gastos'
    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Recordatorio(Base):
    __tablename__ = "recordatorios"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    nota = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

    cliente = relationship("Cliente", back_populates="recordatorios")
