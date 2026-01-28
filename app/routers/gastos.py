
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from datetime import date, timedelta, datetime, timezone

router = APIRouter(prefix="/gastos", tags=["gastos"])



# Endpoint para gastos del día según zona horaria del usuario
@router.get("/del-dia", response_model=list[schemas.Gasto])
def get_gastos_del_dia(offset: int = 0, db: Session = Depends(get_db)):
    """
    offset: minutos de diferencia respecto a UTC (ejemplo: -300 para UTC-5)
    """
    now_utc = datetime.utcnow()
    user_now = now_utc + timedelta(minutes=offset)
    user_today = user_now.date()
    gastos = db.query(models.Gasto).filter(models.Gasto.fecha == user_today).order_by(models.Gasto.fecha.desc()).all()
    return gastos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from datetime import date, timedelta

router = APIRouter(prefix="/gastos", tags=["gastos"])

@router.get("/", response_model=list[schemas.Gasto])
def get_gastos_all(db: Session = Depends(get_db)):
    return db.query(models.Gasto).order_by(models.Gasto.fecha.desc()).all()

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
