from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from datetime import date, timedelta

router = APIRouter(prefix="/gastos", tags=["gastos"])

@router.get("/semana", response_model=list[schemas.Gasto])
def get_gastos_semana(db: Session = Depends(get_db)):
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    gastos = db.query(models.Gasto).filter(models.Gasto.fecha >= inicio_semana).order_by(models.Gasto.fecha.desc()).all()
    return gastos

@router.post("/", response_model=schemas.Gasto)
def create_gasto(gasto: schemas.GastoCreate, db: Session = Depends(get_db)):
    db_gasto = models.Gasto(
        monto=gasto.monto,
        descripcion=gasto.descripcion,
        fecha=gasto.fecha
    )
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto
