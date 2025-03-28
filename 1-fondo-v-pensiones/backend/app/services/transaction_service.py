from typing import List, Dict, Any
from datetime import datetime

class TransactionService:
    def __init__(self):
        # Lista de transacciones (en memoria por ahora)
        self.transactions = []

    async def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Obtiene todas las transacciones"""
        return self.transactions

    async def add_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Agrega una nueva transacción"""
        transaction["id"] = len(self.transactions) + 1
        transaction["timestamp"] = datetime.now().isoformat()
        self.transactions.append(transaction)
        return transaction

transaction_service = TransactionService() 