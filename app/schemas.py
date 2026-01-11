from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ClienteBase(BaseModel):
    nombre: str
    cedula: str
    direccion: str
    negocio: str
    telefono: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    class Config:
        orm_mode = True

class PrestamoBase(BaseModel):
    monto: float
    fecha: date

class PrestamoCreate(PrestamoBase):
    cliente_id: int

class Prestamo(PrestamoBase):
    id: int
    cliente_id: int
    class Config:
        orm_mode = True

class PagoBase(BaseModel):
    monto: float
    fecha: date

class PagoCreate(PagoBase):
    prestamo_id: int

class Pago(PagoBase):
    id: int
    prestamo_id: int
    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
