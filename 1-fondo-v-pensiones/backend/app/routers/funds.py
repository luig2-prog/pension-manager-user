from fastapi import APIRouter
from app.services.fund_service import fund_service

router = APIRouter(
    prefix="/api/funds",
    tags=["funds"]
)

@router.get("/")
async def get_funds():
    """Obtiene todos los fondos disponibles"""
    return await fund_service.get_all_funds()

@router.get("/{fund_id}")
async def get_fund(fund_id: int):
    """Obtiene un fondo específico por su ID"""
    return await fund_service.get_fund(fund_id) 