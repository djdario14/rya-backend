
from fastapi.responses import JSONResponse
# Redeploy trigger
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db, SessionLocal
from datetime import date
from . import models

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import clientes, prestamos, pagos, usuarios, gastos, recordatorios

app = FastAPI()

@app.get("/pagos/dia")
def pagos_del_dia(db: Session = Depends(get_db)):
	hoy = date.today()
	pagos = db.query(models.Pago).filter(models.Pago.fecha == hoy, models.Pago.monto > 0).all()
	resultados = []
	for pago in pagos:
		prestamo = db.query(models.Prestamo).filter(models.Prestamo.id == pago.prestamo_id).first()
		cliente = db.query(models.Cliente).filter(models.Cliente.id == prestamo.cliente_id).first() if prestamo else None
		resultados.append({
			"fecha": pago.fecha.strftime("%Y-%m-%d"),
			"nombre": cliente.nombre if cliente else None,
			"valor": pago.monto
		})
	return JSONResponse(resultados)


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

@app.get("/prestamos/dia")
def prestamos_del_dia(db: Session = Depends(get_db)):
	hoy = date.today()
	prestamos = db.query(models.Prestamo).filter(models.Prestamo.fecha == hoy).all()
	resultados = []
	for prestamo in prestamos:
		cliente = db.query(models.Cliente).filter(models.Cliente.id == prestamo.cliente_id).first()
		interes = round(prestamo.monto * 0.20)
		cuotas = 30  # Asumido fijo, ajusta si es variable
		resultados.append({
			"fecha": prestamo.fecha.strftime("%A, %d %B %Y, %I:%M:%S %p"),
			"nombre": cliente.nombre if cliente else None,
			"valor": int(prestamo.monto),
			"interes": interes,
			"cuotas": cuotas
		})
	return resultados

@app.get("/pagos/dia")
def pagos_del_dia(db: Session = Depends(get_db)):
	hoy = date.today()
	pagos = db.query(models.Pago).filter(models.Pago.fecha == hoy, models.Pago.monto > 0).all()
	resultados = []
	for pago in pagos:
		prestamo = db.query(models.Prestamo).filter(models.Prestamo.id == pago.prestamo_id).first()
		cliente = db.query(models.Cliente).filter(models.Cliente.id == prestamo.cliente_id).first() if prestamo else None
		resultados.append({
			"fecha": pago.fecha.strftime("%Y-%m-%d"),
			"nombre": cliente.nombre if cliente else None,
			"valor": pago.monto
		})
	return JSONResponse(resultados)

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

	# Clientes nuevos hoy
	clientes_nuevos = db.query(models.Cliente).filter(models.Cliente.creado_en == hoy).count()

	return {
		"clientes_con_abono": len(clientes_con_abono),
		"total_clientes": total_clientes,
		"porcentaje_abono": porcentaje_abono,
		"total_a_cobrar": round(total_a_cobrar, 2),
		"caja_inicial": caja_inicial,
		"cobrado_dia": cobrado_dia,
		"prestado_dia": prestado_dia,
		"gastos_dia": gastos_dia,
		"caja_actual": caja_actual,
		"clientes_nuevos": clientes_nuevos
	}

# Endpoint para clientes nuevos del día y semana
from fastapi.responses import JSONResponse
from datetime import timedelta
from fastapi import Query

@app.get("/clientes/nuevos")
def clientes_nuevos(
	db: Session = Depends(get_db),
	periodo: str = Query('dia', enum=['dia', 'semana'])
):
	hoy = date.today()
	if periodo == 'semana':
		inicio_semana = hoy - timedelta(days=hoy.weekday())
		clientes = db.query(models.Cliente).filter(models.Cliente.creado_en >= inicio_semana).all()
	else:
		clientes = db.query(models.Cliente).filter(models.Cliente.creado_en == hoy).all()
	resultado = []
	for c in clientes:
		# Si ubicacion está vacía, usar dirección como coordenadas GPS
		if c.ubicacion:
			ubicacion_url = c.ubicacion
		elif c.direccion and ',' in c.direccion:
			# Construir enlace de Google Maps
			coords = c.direccion.replace(' ', '')
			ubicacion_url = f"https://www.google.com/maps/search/?api=1&query={coords}"
		else:
			ubicacion_url = None
		resultado.append({
			"id": c.id,
			"nombre": c.nombre,
			"fecha": c.creado_en.isoformat() if c.creado_en else None,
			"ubicacion": ubicacion_url
		})
	return JSONResponse(resultado)

@app.get("/ping")
def ping():
	return {"message": "pong"}

@app.get("/clientes/{cliente_id}/prestamos")
def prestamos_direct(cliente_id: int):
	db = SessionLocal()
	try:
		prestamos = db.query(models.Prestamo).filter(models.Prestamo.cliente_id == cliente_id).order_by(models.Prestamo.fecha.desc()).all()
		prestamos_list = []
		for p in prestamos:
			interes = p.monto * 0.20
			total_credito = p.monto + interes
			pagos = db.query(models.Pago).filter(models.Pago.prestamo_id == p.id).all()
			total_abonos = sum(pg.monto for pg in pagos)
			saldo = round(total_credito - total_abonos, 2)
			prestamos_list.append({
				"id": p.id,
				"saldo": saldo,
				"valor": p.monto,
				"fecha": p.fecha,
				"estado": p.estado
			})
		return prestamos_list
	finally:
		db.close()

app.include_router(clientes.router)
app.include_router(prestamos.router)
app.include_router(pagos.router)
app.include_router(usuarios.router)
app.include_router(gastos.router)
app.include_router(recordatorios.router)
