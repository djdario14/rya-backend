

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..database import SessionLocal
from ..models import Pago

router = APIRouter(prefix="/pagos", tags=["pagos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/suma-hoy")
def suma_pagos_hoy(db: Session = Depends(get_db)):
    hoy = date.today()
    # Usar func.date para comparar solo la parte de la fecha (soporta Date y DateTime)
    suma = db.query(Pago).filter(func.date(Pago.fecha) == hoy).with_entities(Pago.monto).all()
    total = sum([p[0] for p in suma])
    return {"total": total}
