from fastapi import APIRouter

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.get("/")
def list_prestamos():
    return ["prestamo1", "prestamo2"]
