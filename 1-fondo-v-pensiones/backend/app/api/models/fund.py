import os
import boto3
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from app.api.models.transaction import TransactionModel

# Datos iniciales de los fondos
INITIAL_FUNDS = [
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

# Simulación de base de datos en memoria
USER_FUNDS = {
    "default_user": {
        "balance": 500000,  # Balance inicial según requisitos
        "subscribed_funds": []
    }
}

class FundModel:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=os.getenv('DYNAMODB_ENDPOINT'))
        self.table = self.dynamodb.Table(os.getenv('FUNDS_TABLE'))
        self.user_funds_table = self.dynamodb.Table(os.getenv('USER_FUNDS_TABLE'))
        self.transactions_table = self.dynamodb.Table(os.getenv('TRANSACTIONS_TABLE'))

    @classmethod
    async def get_all_funds(cls) -> List[Dict]:
        """
        Obtener todos los fondos disponibles
        """
        return INITIAL_FUNDS

    @classmethod
    async def get_fund(cls, fund_id: int) -> Optional[Dict]:
        """
        Obtener un fondo específico por su ID
        """
        for fund in INITIAL_FUNDS:
            if fund["id"] == fund_id:
                return fund
        return None

    @classmethod
    async def get_user_funds(cls, user_id: str) -> Dict:
        """
        Obtener los fondos y balance del usuario
        """
        if user_id not in USER_FUNDS:
            USER_FUNDS[user_id] = {
                "balance": 500000,  # Balance inicial según requisitos
                "subscribed_funds": []
            }
        return USER_FUNDS[user_id]

    @classmethod
    async def subscribe_to_fund(cls, user_id: str, fund_id: int) -> Dict:
        """
        Suscribir a un usuario a un fondo
        """
        # Obtener el fondo
        fund = await cls.get_fund(fund_id)
        if not fund:
            raise ValueError("Fondo no encontrado")

        # Obtener datos del usuario
        user_data = await cls.get_user_funds(user_id)

        # Verificar si ya está suscrito
        if any(f["id"] == str(fund_id) for f in user_data["subscribed_funds"]):
            raise ValueError("Ya está suscrito a este fondo")

        # Verificar saldo suficiente
        if user_data["balance"] < fund["monto_minimo"]:
            raise ValueError(f"No tiene saldo disponible para vincularse al fondo {fund['nombre']}")

        # Crear suscripción
        subscription = {
            "id": str(fund_id),
            "name": fund["nombre"],
            "subscription_date": datetime.now().isoformat(),
            "amount": fund["monto_minimo"]
        }

        # Actualizar saldo y suscripciones
        user_data["balance"] -= fund["monto_minimo"]
        user_data["subscribed_funds"].append(subscription)
        await cls.update_user_funds(user_id, user_data)

        # Registrar la transacción
        transaction = await TransactionModel.add_transaction(
            user_id=user_id,
            fund_id=fund_id,
            transaction_type="SUBSCRIPTION",
            amount=fund["monto_minimo"],
            fund_name=fund["nombre"]
        )

        return {
            "success": True,
            "message": "Suscripción exitosa",
            "transaction_id": transaction["id"],
            "new_balance": user_data["balance"]
        }

    @classmethod
    async def unsubscribe_from_fund(cls, user_id: str, fund_id: str) -> Dict:
        """
        Cancelar la suscripción de un usuario a un fondo
        """
        # Obtener datos del usuario
        user_data = await cls.get_user_funds(user_id)

        # Buscar la suscripción
        subscription = None
        for f in user_data["subscribed_funds"]:
            if f["id"] == fund_id:
                subscription = f
                break

        if not subscription:
            raise ValueError("No está suscrito a este fondo")

        # Devolver el monto al balance
        user_data["balance"] += subscription["amount"]
        user_data["subscribed_funds"] = [
            f for f in user_data["subscribed_funds"] if f["id"] != fund_id
        ]
        await cls.update_user_funds(user_id, user_data)

        # Registrar la transacción
        transaction = await TransactionModel.add_transaction(
            user_id=user_id,
            fund_id=int(fund_id),
            transaction_type="CANCELLATION",
            amount=subscription["amount"],
            fund_name=subscription["name"]
        )

        return {
            "success": True,
            "message": "Cancelación exitosa",
            "transaction_id": transaction["id"],
            "new_balance": user_data["balance"]
        }

    @classmethod
    async def update_user_funds(cls, user_id: str, user_data: Dict):
        """
        Actualizar los fondos y balance del usuario en la base de datos en memoria
        """
        USER_FUNDS[user_id] = user_data