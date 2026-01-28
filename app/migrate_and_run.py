import subprocess

# Ejecuta la migración de Alembic
subprocess.run(["alembic", "upgrade", "head"], check=True)

# Arranca el servidor Uvicorn normalmente
import uvicorn
uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
