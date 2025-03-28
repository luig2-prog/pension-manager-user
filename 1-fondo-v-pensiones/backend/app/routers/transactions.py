from fastapi import APIRouter

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

@router.get("/")
async def get_transactions():
    """Obtiene todas las transacciones"""
    # Por implementar
    return {"message": "Endpoint de transacciones por implementar"} 