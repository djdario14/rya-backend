from pydantic import BaseModel

# --- Cliente con saldo para endpoint especial ---
class ClienteConSaldo(BaseModel):
    id: int
    nombre: str
    cedula: str
    direccion: str
    negocio: str
    telefono: str
    saldo: float

    class Config:
        from_attributes = True
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
        from_attributes = True

class PrestamoBase(BaseModel):
    monto: float
    fecha: date
    estado: str = 'activo'
    interes: float = 0
    total: float = 0
    cuotas: int = 0
    valor_cuota: float = 0
    forma_pago: str = 'Diario'

class PrestamoCreate(PrestamoBase):
    cliente_id: int

class Prestamo(PrestamoBase):
    id: int
    cliente_id: int
    class Config:
        from_attributes = True


class PagoBase(BaseModel):
    monto: float | None = None
    fecha: date
    motivo_no_pago: str | None = None


class PagoCreate(PagoBase):
    prestamo_id: int


class Pago(PagoBase):
    id: int
    prestamo_id: int
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str


class GastoBase(BaseModel):
    monto: float
    descripcion: str
    fecha: date

class GastoCreate(GastoBase):
    pass

class Gasto(GastoBase):
    id: int
    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True
