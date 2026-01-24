from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.get("/activo/{cliente_id}")
def get_prestamo_activo(cliente_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id, models.Prestamo.estado == 'activo').order_by(models.Prestamo.id.desc()).first()
    if not prestamo:
        return {}
    return {
        "id": prestamo.id,
        "cliente_id": prestamo.cliente_id,
        "monto": prestamo.monto,
        "fecha": prestamo.fecha,
        "estado": prestamo.estado,
        "interes": prestamo.interes,
        "total": prestamo.total,
        "cuotas": prestamo.cuotas,
        "valor_cuota": prestamo.valor_cuota,
        "forma_pago": prestamo.forma_pago
    }
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    try:
        total = prestamo.monto + prestamo.interes
        db_prestamo = models.Prestamo(
            cliente_id=prestamo.cliente_id,
            monto=prestamo.monto,
            fecha=prestamo.fecha,
            estado=getattr(prestamo, 'estado', 'activo'),
            interes=prestamo.interes,
            total=total,
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
