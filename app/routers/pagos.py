from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..database import get_db
from .. import models, schemas


router = APIRouter(prefix="/pagos", tags=["pagos"])

# Endpoint para obtener pagos por cliente
@router.get("/cliente/{cliente_id}", response_model=list[schemas.Pago])
def get_pagos_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    prestamos = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id).all()
    pagos = []
    for prestamo in prestamos:
        pagos += db.query(models.Pago).filter(models.Pago.prestamo_id == prestamo.id).all()
    return pagos

# Endpoint para sumar pagos de hoy
@router.get("/suma-hoy")
def suma_pagos_hoy(db: Session = Depends(get_db)):
    hoy = date.today()
    suma = db.query(models.Pago).filter(func.date(models.Pago.fecha) == hoy).with_entities(models.Pago.monto).all()
    total = sum([p[0] for p in suma])
    return {"total": total}

# Endpoint para detalle de pagos de hoy (cliente y monto)
@router.get("/hoy-detalle")
def pagos_hoy_detalle(db: Session = Depends(get_db)):
    hoy = date.today()
    pagos = (
        db.query(models.Pago, models.Prestamo, models.Cliente)
        .join(models.Prestamo, models.Pago.prestamo_id == models.Prestamo.id)
        .join(models.Cliente, models.Prestamo.cliente_id == models.Cliente.id)
        .filter(func.date(models.Pago.fecha) == hoy)
        .with_entities(models.Cliente.nombre, models.Pago.monto)
        .all()
    )
    return [{"cliente": nombre, "monto": monto} for nombre, monto in pagos]

@router.get("/")
def list_pagos():
    return ["pago1", "pago2"]

@router.post("/", response_model=schemas.Pago)
def create_pago(pago: schemas.PagoCreate, db: Session = Depends(get_db)):
    db_prestamo = db.query(models.Prestamo).filter(models.Prestamo.id == pago.prestamo_id).first()
    if not db_prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    db_pago = models.Pago(
        prestamo_id=pago.prestamo_id,
        monto=pago.monto if pago.monto is not None else 0,
        fecha=pago.fecha,
        motivo_no_pago=pago.motivo_no_pago
    )
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)

    # Verificar si el saldo del préstamo llegó a 0 y actualizar estado a 'pagado'
    pagos = db.query(models.Pago).filter(models.Pago.prestamo_id == pago.prestamo_id).all()
    total_abonado = sum(p.monto for p in pagos)
    saldo = (db_prestamo.total or 0) - total_abonado
    if saldo <= 0 and db_prestamo.estado != 'pagado':
        db_prestamo.estado = 'pagado'
        db.commit()

    return db_pago
