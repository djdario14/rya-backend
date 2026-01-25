from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from .. import models, schemas, database
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/clientes", tags=["clientes"])

# Endpoint exclusivo para clientes pendientes (no han abonado hoy)
@router.get("/pendientes")
def clientes_pendientes():
    db = database.SessionLocal()
    clientes = db.query(models.Cliente).all()
    hoy = date.today()
    pendientes = []
    for cliente in clientes:
        prestamos = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente.id).all()
        pago_hoy = False
        if prestamos:
            pagos = db.query(models.Pago).filter(models.Pago.prestamo_id.in_([p.id for p in prestamos])).all()
            if pagos:
                fechas_pago = [str(p.fecha) for p in pagos if p.fecha is not None]
                pago_hoy = str(hoy) in fechas_pago
        if not pago_hoy:
            pendientes.append({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "saldo": 0
            })
    return JSONResponse(content=jsonable_encoder(pendientes))

# --- Endpoint especial debe ir antes de endpoints dinámicos ---
@router.get("/con-ultimo-pago")
def list_clientes_con_ultimo_pago():
    db = database.SessionLocal()
    clientes = db.query(models.Cliente).all()
    result = []
    hoy = date.today()
    for cliente in clientes:
        prestamos = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente.id).all()
        ultimo_pago = None
        pago_hoy = False
        if prestamos:
            pagos = db.query(models.Pago).filter(models.Pago.prestamo_id.in_([p.id for p in prestamos])).all()
            if pagos:
                fechas_pago = [p.fecha for p in pagos if p.fecha is not None]
                if fechas_pago:
                    # Convertir fechas a string para comparación y serialización
                    fechas_pago_str = [str(pf) for pf in fechas_pago]
                    ultimo_pago = max(fechas_pago_str)
                    pago_hoy = str(hoy) in fechas_pago_str
        result.append({
            "id": cliente.id,
            "nombre": cliente.nombre,
            "saldo": 0,
            "ultimo_pago": str(ultimo_pago) if ultimo_pago else None,
            "pago_hoy": pago_hoy
        })
    print("DEBUG /clientes/con-ultimo-pago", result)
    return JSONResponse(content=jsonable_encoder(result))

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
