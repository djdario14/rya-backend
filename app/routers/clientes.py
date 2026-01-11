from fastapi import APIRouter

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/")
def list_clientes():
    return ["cliente1", "cliente2"]
