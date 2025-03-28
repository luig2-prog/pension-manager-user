from typing import Optional, Dict, Any, List

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
        # Lista de suscripciones (en memoria por ahora)
        self.subscriptions = []

    async def get_fund(self, fund_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un fondo por su ID"""
        return next((fund for fund in self.funds if fund["id"] == fund_id), None)

    async def get_all_funds(self) -> list:
        """Obtiene todos los fondos disponibles"""
        return self.funds

    async def get_user_subscriptions(self) -> Dict[str, Any]:
        """Obtiene las suscripciones del usuario actual"""
        # Por ahora retornamos todas las suscripciones
        # En producción, filtraríamos por el usuario actual
        subscribed_fund_ids = [sub["fund_id"] for sub in self.subscriptions]
        
        return {
            "balance": 500000,  # Balance simulado
            "subscribed_funds": subscribed_fund_ids
        }

    async def subscribe(self, fund_id: int) -> Dict[str, Any]:
        """Suscribe un usuario a un fondo"""
        fund = await self.get_fund(fund_id)
        if not fund:
            raise ValueError(f"Fondo con ID {fund_id} no encontrado")
        
        # Aquí normalmente validaríamos el usuario y otros detalles
        subscription = {
            "id": len(self.subscriptions) + 1,
            "fund_id": fund_id,
            "status": "active",
            "created_at": "2024-03-28T00:00:00Z"  # En producción usar datetime.now()
        }
        
        self.subscriptions.append(subscription)
        return subscription

    async def unsubscribe(self, fund_id: int) -> Dict[str, Any]:
        """Cancela la suscripción de un usuario a un fondo"""
        fund = await self.get_fund(fund_id)
        if not fund:
            raise ValueError(f"Fondo con ID {fund_id} no encontrado")
        
        # Buscar y eliminar la suscripción
        subscription = next((sub for sub in self.subscriptions if sub["fund_id"] == fund_id), None)
        if not subscription:
            raise ValueError(f"No existe una suscripción activa para el fondo con ID {fund_id}")
        
        self.subscriptions = [sub for sub in self.subscriptions if sub["fund_id"] != fund_id]
        return {
            "message": f"Suscripción al fondo {fund['nombre']} cancelada exitosamente",
            "fund_id": fund_id
        }

fund_service = FundService() 