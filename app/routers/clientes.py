
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from sqlalchemy import func

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/")
def list_clientes():
    db = database.SessionLocal()
    try:
        clientes = db.query(models.Cliente).all()
        # Devuelve id y nombre
        return [{"id": c.id, "nombre": c.nombre} for c in clientes]
    finally:
        db.close()

# Nuevo endpoint para obtener saldo de un cliente
@router.get("/{cliente_id}/saldo")
def get_cliente_saldo(cliente_id: int):
    db = database.SessionLocal()
    try:
        prestamo = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id, models.Prestamo.estado == 'activo').order_by(models.Prestamo.id.desc()).first()
        if not prestamo:
            return {"saldo": 0.0, "prestamo": 0.0, "cuotasTotal": 0, "cuotasPagadas": 0, "atraso": 0}

        monto = prestamo.monto
        # Interés: 20% fijo (puedes cambiar esto si lo guardas en la BD)
        interes = monto * 0.20
        total_credito = monto + interes

        # Cuotas registradas en el préstamo
        cuotas_total = getattr(prestamo, 'cuotas', 30)  # Si no existe el campo, por defecto 30

        # Pagos realizados
        pagos = db.query(models.Pago).filter(models.Pago.prestamo_id == prestamo.id).all()
        total_abonos = sum(p.monto for p in pagos)
        cuotas_pagadas = len(pagos)

        # Saldo actual
        saldo = total_credito - total_abonos

        # Atraso: días desde la fecha del préstamo hasta hoy, menos los días con abono
        from datetime import date
        dias_transcurridos = (date.today() - prestamo.fecha).days
        # Si pagó hoy, no cuenta como atraso
        dias_sin_abono = dias_transcurridos - cuotas_pagadas
        # Si ya terminó de pagar, atraso es 0
        atraso = max(0, dias_sin_abono) if saldo > 0 else 0

        return {
            "saldo": round(saldo, 2),
            "prestamo": monto,
            "cuotasTotal": cuotas_total,
            "cuotasPagadas": cuotas_pagadas,
            "atraso": atraso
        }
    finally:
        db.close()

# Endpoint para obtener un cliente por id
@router.get("/{cliente_id}", response_model=schemas.Cliente)
def get_cliente(cliente_id: int):
    db = database.SessionLocal()
    try:
        cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    finally:
        db.close()
@router.get("/{cliente_id}", response_model=schemas.Cliente)
def get_cliente(cliente_id: int):
    db = database.SessionLocal()
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

    monto = prestamo.monto
    # Interés: 20% fijo (puedes cambiar esto si lo guardas en la BD)
    interes = monto * 0.20
    total_credito = monto + interes

    # Cuotas registradas en el préstamo
    cuotas_total = getattr(prestamo, 'cuotas', 30)  # Si no existe el campo, por defecto 30

    # Pagos realizados
    pagos = db.query(models.Pago).filter(models.Pago.prestamo_id == prestamo.id).all()
    total_abonos = sum(p.monto for p in pagos)
    cuotas_pagadas = len(pagos)

    # Saldo actual
    saldo = total_credito - total_abonos

    # Atraso: días desde la fecha del préstamo hasta hoy, menos los días con abono
    from datetime import date
    dias_transcurridos = (date.today() - prestamo.fecha).days
    # Si pagó hoy, no cuenta como atraso
    dias_sin_abono = dias_transcurridos - cuotas_pagadas
    # Si ya terminó de pagar, atraso es 0
    atraso = max(0, dias_sin_abono) if saldo > 0 else 0

    return {
        "saldo": round(saldo, 2),
        "prestamo": monto,
        "cuotasTotal": cuotas_total,
        "cuotasPagadas": cuotas_pagadas,
        "atraso": atraso
    }

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
