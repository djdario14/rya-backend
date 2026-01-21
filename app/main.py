
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
		"https://rya-backend-production.up.railway.app",
		"https://rya-cobranza.netlify.app"  # <--- Agregado dominio de Netlify
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(prestamos.router)
app.include_router(pagos.router)
app.include_router(usuarios.router)
app.include_router(gastos.router)
