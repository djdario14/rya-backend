
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
    ahora = datetime.now()
    recs = db.query(models.Recordatorio).filter(models.Recordatorio.fecha <= ahora, models.Recordatorio.leido == 0).order_by(models.Recordatorio.fecha.asc()).all()
    # Enriquecer con nombre de cliente si está disponible
    return recs

@router.post("/marcar_leido/{recordatorio_id}")
def marcar_recordatorio_leido(recordatorio_id: int, db: Session = Depends(get_db)):
    rec = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    rec.leido = 1
    db.commit()
    return {"ok": True}
