from fastapi import APIRouter

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def list_usuarios():
    return ["usuario1", "usuario2"]
