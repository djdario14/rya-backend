# Redeploy trigger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import clientes, prestamos, pagos, usuarios, gastos

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"https://rya-cobranza.vercel.app",
		"https://rya-git-main-djdario14s-projects.vercel.app",
		"https://rya-fronted.vercel.app",
		"http://localhost:3000",
		"http://127.0.0.1:3000",
		"https://rya-backend-production.up.railway.app"
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db
from datetime import date
from . import models

@app.get("/reporte/diario")
def reporte_diario(db: Session = Depends(get_db)):
	hoy = date.today()
	# Total de clientes
	total_clientes = db.query(models.Cliente).count()
	# Clientes con abono hoy
	pagos_hoy = db.query(models.Pago).filter(models.Pago.fecha == hoy, models.Pago.monto > 0).all()
	clientes_con_abono = set()
	for pago in pagos_hoy:
		prestamo = db.query(models.Prestamo).filter(models.Prestamo.id == pago.prestamo_id).first()
		if prestamo:
			clientes_con_abono.add(prestamo.cliente_id)
	porcentaje_abono = round((len(clientes_con_abono) / total_clientes) * 100, 2) if total_clientes else 0
	# Total a cobrar (suma de cuotas de todos los préstamos activos)
	prestamos_activos = db.query(models.Prestamo).filter(models.Prestamo.estado == 'activo').all()
	total_a_cobrar = sum(p.monto * 1.2 / 30 for p in prestamos_activos)  # cuota diaria estimada
	# Caja inicial (puedes ajustar la lógica según tu sistema)
	caja_inicial = 4149  # Valor fijo de ejemplo, deberías traerlo de la BD o config
	# Cobrado hoy
	cobrado_dia = sum(p.monto for p in pagos_hoy)
	# Prestado hoy
	prestado_dia = sum(p.monto for p in db.query(models.Prestamo).filter(models.Prestamo.fecha == hoy).all())
	# Gastos hoy
	gastos_dia = sum(g.monto for g in db.query(models.Gasto).filter(models.Gasto.fecha == hoy).all())
	# Caja actual
	caja_actual = caja_inicial + cobrado_dia - gastos_dia - prestado_dia
	return {
		"clientes_con_abono": len(clientes_con_abono),
		"total_clientes": total_clientes,
		"porcentaje_abono": porcentaje_abono,
		"total_a_cobrar": round(total_a_cobrar, 2),
		"caja_inicial": caja_inicial,
		"cobrado_dia": cobrado_dia,
		"prestado_dia": prestado_dia,
		"gastos_dia": gastos_dia,
		"caja_actual": caja_actual
	}

@app.get("/ping")
def ping():
    return {"message": "pong"}

import sys

try:
    print('Incluyendo router de clientes...', file=sys.stderr)
    app.include_router(clientes.router)
    print('Incluido router de clientes', file=sys.stderr)
except Exception as e:
    print(f'Error en clientes.router: {e}', file=sys.stderr)

try:
    print('Incluyendo router de prestamos...', file=sys.stderr)
    app.include_router(prestamos.router)
    print('Incluido router de prestamos', file=sys.stderr)
except Exception as e:
    print(f'Error en prestamos.router: {e}', file=sys.stderr)

try:
    print('Incluyendo router de pagos...', file=sys.stderr)
    app.include_router(pagos.router)
    print('Incluido router de pagos', file=sys.stderr)
except Exception as e:
    print(f'Error en pagos.router: {e}', file=sys.stderr)

try:
    print('Incluyendo router de usuarios...', file=sys.stderr)
    app.include_router(usuarios.router)
    print('Incluido router de usuarios', file=sys.stderr)
except Exception as e:
    print(f'Error en usuarios.router: {e}', file=sys.stderr)

try:
    print('Incluyendo router de gastos...', file=sys.stderr)
    app.include_router(gastos.router)
    print('Incluido router de gastos', file=sys.stderr)
except Exception as e:
    print(f'Error en gastos.router: {e}', file=sys.stderr)
