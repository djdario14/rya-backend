from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/")
def list_clientes():
    db = database.SessionLocal()
    clientes = db.query(models.Cliente).all()
    return [c.nombre for c in clientes]

@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteBase):
    db = database.SessionLocal()
    db_cliente = models.Cliente(
        nombre=cliente.nombre,
        cedula=cliente.cedula,
        direccion=cliente.direccion,
        negocio=cliente.negocio,
        telefono=cliente.telefono
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
