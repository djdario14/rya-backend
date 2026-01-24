from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.get("/")
def list_prestamos():
    return ["prestamo1", "prestamo2"]

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
            estado=getattr(prestamo, 'estado', 'activo'),
            interes=prestamo.interes,
            total=prestamo.total,
            cuotas=prestamo.cuotas,
            valor_cuota=prestamo.valor_cuota,
            forma_pago=prestamo.forma_pago
        )
        db.add(db_prestamo)
        db.commit()
        db.refresh(db_prestamo)
        return db_prestamo
    except Exception as e:
        print("Error al registrar préstamo:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
