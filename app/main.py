from fastapi import FastAPI
from .routers import clientes, prestamos, pagos, usuarios

app = FastAPI()

app.include_router(clientes.router)
app.include_router(prestamos.router)
app.include_router(pagos.router)
app.include_router(usuarios.router)
