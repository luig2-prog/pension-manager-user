from typing import Dict, List, Any
import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime

# Configure DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', None)
)

# DynamoDB transactions table
transactions_table = dynamodb.Table(os.environ.get('TRANSACTIONS_TABLE', 'Transactions'))

# Simulación de base de datos en memoria para transacciones
TRANSACTIONS = []

class TransactionModel:
    @staticmethod
    async def get_transactions(user_id: str = "default_user") -> List[Dict[str, Any]]:
        """Get all transactions for a user"""
        try:
            response = transactions_table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
            # Sort by timestamp descending (latest first)
            transactions = response.get('Items', [])
            transactions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return transactions
        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            return []
    
    @staticmethod
    async def get_transaction(transaction_id: str) -> Dict[str, Any]:
        """Get a specific transaction by ID"""
        try:
            response = transactions_table.query(
                IndexName="id-index",
                KeyConditionExpression=Key('id').eq(transaction_id)
            )
            items = response.get('Items', [])
            if items:
                return items[0]
            return {}
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {str(e)}")
            return {}

    @classmethod
    async def add_transaction(cls, user_id: str, fund_id: int, transaction_type: str, amount: float, fund_name: str) -> Dict:
        """
        Agregar una nueva transacción
        """
        transaction = {
            "id": f"{transaction_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "fund_id": fund_id,
            "fund_name": fund_name,
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }
        TRANSACTIONS.append(transaction)
        return transaction

    @classmethod
    async def get_user_transactions(cls, user_id: str) -> List[Dict]:
        """
        Obtener todas las transacciones de un usuario ordenadas por fecha descendente
        """
        user_transactions = [t for t in TRANSACTIONS if t["user_id"] == user_id]
        return sorted(user_transactions, key=lambda x: x["timestamp"], reverse=True) 