from fastapi import APIRouter

router = APIRouter(prefix="/pagos", tags=["pagos"])

@router.get("/")
def list_pagos():
    return ["pago1", "pago2"]
