@router.get("/hoy-detalle")
def prestamos_hoy_detalle(db: Session = Depends(get_db)):
    hoy = date.today()
    prestamos = db.query(models.Prestamo, models.Cliente).join(models.Cliente, models.Prestamo.cliente_id == models.Cliente.id)
    prestamos = prestamos.filter(func.date(models.Prestamo.fecha) == hoy).all()
    resultado = []
    for p, c in prestamos:
        resultado.append({
            "cliente": c.nombre,
            "monto": p.monto,
            "forma_pago": p.forma_pago,
            "cuotas": p.cuotas,
            "valor_cuota": p.valor_cuota
        })
    return resultado

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..database import get_db
from .. import models, schemas
from typing import List
import traceback

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

# Endpoint para suma de préstamos de hoy (solo monto)
@router.get("/suma-hoy")
def suma_prestamos_hoy(db: Session = Depends(get_db)):
    hoy = date.today()
    prestamos = db.query(models.Prestamo).filter(func.date(models.Prestamo.fecha) == hoy).all()
    total = sum([(p.monto or 0) for p in prestamos])
    return {"total": total}

@router.get("/activo/{cliente_id}")
def get_prestamo_activo(cliente_id: int, db: Session = Depends(get_db)):
# ...existing code...
    prestamo = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id, models.Prestamo.estado == 'activo').order_by(models.Prestamo.id.desc()).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="No hay préstamo activo para este cliente")
# Mover la definición de router antes de su uso
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..database import get_db
from .. import models, schemas
from typing import List
import traceback

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

# Endpoint para detalle de préstamos del día actual
@router.get("/hoy-detalle")
def prestamos_hoy_detalle(db: Session = Depends(get_db)):
    hoy = date.today()
    prestamos = db.query(models.Prestamo, models.Cliente).join(models.Cliente, models.Prestamo.cliente_id == models.Cliente.id)
    prestamos = prestamos.filter(func.date(models.Prestamo.fecha) == hoy).all()
    resultado = []
    for p, c in prestamos:
        resultado.append({
            "cliente": c.nombre,
            "monto": p.monto,
            "forma_pago": p.forma_pago,
            "cuotas": p.cuotas,
            "valor_cuota": p.valor_cuota
        })
    return resultado
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

# Endpoint para registrar un préstamo
@router.post("/", response_model=schemas.Prestamo)
def create_prestamo(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == prestamo.cliente_id).first()
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
