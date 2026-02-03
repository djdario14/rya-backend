
# --- IMPORTS ---
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from datetime import date

# --- ROUTER DEFINITION ---
router = APIRouter(
    prefix="/recordatorios",
    tags=["recordatorios"]
)

# --- ENDPOINTS ---
@router.get("/", response_model=list[schemas.Recordatorio])
def get_all_recordatorios(db: Session = Depends(get_db)):
    import pytz
    records = db.query(models.Recordatorio).all()
    # Convertir fechas a ISO 8601 con zona horaria UTC
    for r in records:
        if r.fecha and r.fecha.tzinfo is None:
            r.fecha = pytz.utc.localize(r.fecha)
        if r.creado_en and r.creado_en.tzinfo is None:
            r.creado_en = pytz.utc.localize(r.creado_en)
    return records


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from datetime import date

router = APIRouter(
    prefix="/recordatorios",
    tags=["recordatorios"]
)

@router.get("/", response_model=list[schemas.Recordatorio])
def get_all_recordatorios(db: Session = Depends(get_db)):
    return db.query(models.Recordatorio).all()

@router.get("/", response_model=list[schemas.Recordatorio])
def get_all_recordatorios(db: Session = Depends(get_db)):
    return db.query(models.Recordatorio).all()

@router.post("/", response_model=schemas.Recordatorio)
def create_recordatorio(recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    # Convertir fecha local (sin zona horaria) a UTC
    from datetime import datetime
    import pytz
    # Asumimos que la fecha recibida es local (America/Guayaquil)
    local_tz = pytz.timezone("America/Guayaquil")
    # Si la fecha ya tiene zona horaria, no hace nada; si no, la agrega como local
    if recordatorio.fecha.tzinfo is None:
        dt_local = local_tz.localize(recordatorio.fecha)
    else:
        dt_local = recordatorio.fecha.astimezone(local_tz)
    dt_utc = dt_local.astimezone(pytz.utc)
    data = recordatorio.dict()
    data['fecha'] = dt_utc
    db_recordatorio = models.Recordatorio(**data)
    db.add(db_recordatorio)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@router.get("/cliente/{cliente_id}", response_model=list[schemas.Recordatorio])
def get_recordatorios_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return db.query(models.Recordatorio).filter(models.Recordatorio.cliente_id == cliente_id).all()

@router.get("/{id}", response_model=schemas.Recordatorio)
def get_recordatorio(id: int, db: Session = Depends(get_db)):
    recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == id).first()
    if not recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    return recordatorio

@router.put("/{id}", response_model=schemas.Recordatorio)
def update_recordatorio(id: int, recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == id).first()
    if not db_recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    for key, value in recordatorio.dict().items():
        setattr(db_recordatorio, key, value)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@router.delete("/{id}")
def delete_recordatorio(id: int, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == id).first()
    if not db_recordatorio:
        raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
    db.delete(db_recordatorio)
    db.commit()
    return {"ok": True}
