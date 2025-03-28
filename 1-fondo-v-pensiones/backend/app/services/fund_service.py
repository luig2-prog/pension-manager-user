from typing import Optional, Dict, Any

class FundService:
    def __init__(self):
        # Lista de fondos disponibles
        self.funds = [
            {
                "id": 1,
                "nombre": "FPV_EL_CLIENTE_RECAUDADORA",
                "monto_minimo": 75000,
                "categoria": "FPV"
            },
            {
                "id": 2,
                "nombre": "FPV_EL_CLIENTE_ECOPETROL",
                "monto_minimo": 125000,
                "categoria": "FPV"
            },
            {
                "id": 3,
                "nombre": "DEUDAPRIVADA",
                "monto_minimo": 50000,
                "categoria": "FIC"
            },
            {
                "id": 4,
                "nombre": "FDO-ACCIONES",
                "monto_minimo": 250000,
                "categoria": "FIC"
            },
            {
                "id": 5,
                "nombre": "FPV_EL CLIENTE_DINAMICA",
                "monto_minimo": 100000,
                "categoria": "FPV"
            }
        ]

    async def get_fund(self, fund_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un fondo por su ID"""
        return next((fund for fund in self.funds if fund["id"] == fund_id), None)

    async def get_all_funds(self) -> list:
        """Obtiene todos los fondos disponibles"""
        return self.funds

fund_service = FundService() 