from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    cedula = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    negocio = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    prestamos = relationship('Prestamo', back_populates='cliente')

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    monto = Column(Float)
    fecha = Column(Date)
    estado = Column(String, nullable=False, default='activo')
    interes = Column(Float, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    cuotas = Column(Integer, nullable=False, default=0)
    valor_cuota = Column(Float, nullable=False, default=0)
    forma_pago = Column(String, nullable=False, default='Diario')
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
