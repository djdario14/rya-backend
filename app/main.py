
# Redeploy trigger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import clientes, prestamos, pagos, usuarios

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"https://rya-cobranza.vercel.app"
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(prestamos.router)
app.include_router(pagos.router)
app.include_router(usuarios.router)
