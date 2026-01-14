from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.get("/")
def list_prestamos(cliente_id: int = Query(None), estado: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Prestamo)
    if cliente_id is not None:
        query = query.filter(models.Prestamo.cliente_id == cliente_id)
    if estado is not None:
        query = query.filter(models.Prestamo.estado == estado)
    prestamos = query.all()
    return [
        {
            "id": p.id,
            "cliente_id": p.cliente_id,
            "monto": p.monto,
            "fecha": p.fecha.isoformat() if p.fecha else None,
            "estado": p.estado
        }
        for p in prestamos
    ]

# Nuevo endpoint para crear préstamos
@router.post("/", response_model=schemas.Prestamo)
def create_prestamo(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    import traceback
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == prestamo.cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    try:
        db_prestamo = models.Prestamo(
            cliente_id=prestamo.cliente_id,
            monto=prestamo.monto,
            fecha=prestamo.fecha,
            estado=getattr(prestamo, 'estado', 'activo')
        )
        db.add(db_prestamo)
        db.commit()
        db.refresh(db_prestamo)
        return db_prestamo
    except Exception as e:
        print("Error al registrar préstamo:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
