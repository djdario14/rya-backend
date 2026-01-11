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
    prestamos = relationship('Prestamo', back_populates='cliente')

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    monto = Column(Float)
    fecha = Column(Date)
    cliente = relationship('Cliente', back_populates='prestamos')
    pagos = relationship('Pago', back_populates='prestamo')

class Pago(Base):
    __tablename__ = 'pagos'
    id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey('prestamos.id'))
    monto = Column(Float)
    fecha = Column(Date)
    prestamo = relationship('Prestamo', back_populates='pagos')

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
