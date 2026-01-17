from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, database

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RecordatorioOut)
def crear_recordatorio(recordatorio: schemas.RecordatorioCreate, cliente_id: int, db: Session = Depends(get_db)):
    db_recordatorio = models.Recordatorio(
        cliente_id=cliente_id,
        fecha=recordatorio.fecha,
        nota=recordatorio.nota
    )
    db.add(db_recordatorio)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@router.get("/cliente/{cliente_id}", response_model=list[schemas.RecordatorioOut])
def listar_recordatorios(cliente_id: int, db: Session = Depends(get_db)):
    return db.query(models.Recordatorio).filter(models.Recordatorio.cliente_id == cliente_id).order_by(models.Recordatorio.fecha.desc()).all()

@router.get("/pendientes", response_model=list[schemas.RecordatorioOut])
def recordatorios_pendientes(db: Session = Depends(get_db)):
    hoy = datetime.now()
    recs = db.query(models.Recordatorio).filter(models.Recordatorio.fecha >= hoy).order_by(models.Recordatorio.fecha.asc()).all()
    # Enriquecer con nombre de cliente si está disponible
    for r in recs:
        if hasattr(r, 'cliente') and r.cliente:
            r.cliente_nombre = r.cliente.nombre
    return recs
