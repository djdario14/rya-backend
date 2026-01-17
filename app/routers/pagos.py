from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
    return db_pago
