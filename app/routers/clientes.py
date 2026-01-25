from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/clientes", tags=["clientes"])
from sqlalchemy.orm import Session
from .. import models, schemas, database
from sqlalchemy import func

# --- ENDPOINTS FIJOS ANTES DE LOS DINÁMICOS ---
from typing import List
@router.get("/con-saldo", response_model=List[schemas.ClienteConSaldo])
def list_clientes_con_saldo():
    db = database.SessionLocal()
    try:
        clientes = db.query(models.Cliente).all()
        clientes_con_saldo = []
        for cliente in clientes:
            # Préstamos activos del cliente
            prestamos = db.query(models.Prestamo).filter(
                models.Prestamo.cliente_id == cliente.id,
                models.Prestamo.estado == "activo"
            ).all()
            monto_total = sum(p.monto + p.interes for p in prestamos)
            pagos = db.query(models.Pago).filter(
                models.Pago.prestamo_id.in_([p.id for p in prestamos])
            ).all() if prestamos else []
            total_pagado = sum(p.monto for p in pagos)
            saldo = monto_total - total_pagado
            cliente_dict = cliente.__dict__.copy()
            cliente_dict["saldo"] = saldo
            clientes_con_saldo.append(cliente_dict)
        return clientes_con_saldo
    finally:
        db.close()

# --- ENDPOINTS DINÁMICOS AL FINAL ---


# --- ENDPOINTS DINÁMICOS AL FINAL ---
@router.get("/{cliente_id}/saldo")
def get_cliente_saldo(cliente_id: int):
    db = database.SessionLocal()
    try:
        prestamo = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id, models.Prestamo.estado == 'activo').order_by(models.Prestamo.id.desc()).first()
        if not prestamo:
            return {"saldo": 0.0, "prestamo": 0.0, "cuotasTotal": 0, "cuotasPagadas": 0, "atraso": 0, "fecha": None}

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
            "atraso": atraso,
            "fecha": prestamo.fecha.isoformat() if prestamo and prestamo.fecha else None
        }
    finally:
        db.close()

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
