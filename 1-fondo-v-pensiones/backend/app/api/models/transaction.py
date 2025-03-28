from typing import Dict, List, Any
import boto3
from boto3.dynamodb.conditions import Key
import os

# Configure DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', None)
)

# DynamoDB transactions table
transactions_table = dynamodb.Table(os.environ.get('TRANSACTIONS_TABLE', 'Transactions'))

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