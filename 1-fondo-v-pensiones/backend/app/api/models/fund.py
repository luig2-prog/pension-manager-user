from typing import Dict, List, Optional, Any
import boto3
from boto3.dynamodb.conditions import Key
import os
import uuid
from datetime import datetime

# Configure DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', None)
)

# DynamoDB tables
funds_table = dynamodb.Table(os.environ.get('FUNDS_TABLE', 'Funds'))
user_funds_table = dynamodb.Table(os.environ.get('USER_FUNDS_TABLE', 'UserFunds'))
transactions_table = dynamodb.Table(os.environ.get('TRANSACTIONS_TABLE', 'Transactions'))

# Initial funds data
INITIAL_FUNDS = [
    {
        "id": "1",
        "name": "FPV_EL CLIENTE_RECAUDADORA",
        "min_amount": 75000,
        "category": "FPV"
    },
    {
        "id": "2",
        "name": "FPV_EL CLIENTE_ECOPETROL",
        "min_amount": 125000,
        "category": "FPV"
    },
    {
        "id": "3",
        "name": "DEUDAPRIVADA",
        "min_amount": 50000,
        "category": "FIC"
    },
    {
        "id": "4",
        "name": "FDO-ACCIONES",
        "min_amount": 250000,
        "category": "FIC"
    },
    {
        "id": "5",
        "name": "FPV_EL CLIENTE_DINAMICA",
        "min_amount": 100000,
        "category": "FPV"
    }
]

# Initial user balance
INITIAL_BALANCE = 500000

class FundModel:
    @staticmethod
    async def initialize_database():
        """Initialize the database with seed data if needed"""
        try:
            # Check if funds exist, if not, create them
            response = funds_table.scan(Limit=1)
            if not response.get('Items'):
                with funds_table.batch_writer() as batch:
                    for fund in INITIAL_FUNDS:
                        batch.put_item(Item=fund)
            
            # Check if user account exists, if not, create it
            response = user_funds_table.get_item(Key={"user_id": "default_user"})
            if "Item" not in response:
                user_funds_table.put_item(
                    Item={
                        "user_id": "default_user",
                        "balance": INITIAL_BALANCE,
                        "subscribed_funds": []
                    }
                )
            return True
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            return False

    @staticmethod
    async def get_all_funds() -> List[Dict[str, Any]]:
        """Get all available funds"""
        try:
            response = funds_table.scan()
            return response.get('Items', [])
        except Exception as e:
            print(f"Error getting funds: {str(e)}")
            return []

    @staticmethod
    async def get_fund(fund_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific fund by ID"""
        try:
            response = funds_table.get_item(Key={"id": fund_id})
            return response.get('Item')
        except Exception as e:
            print(f"Error getting fund {fund_id}: {str(e)}")
            return None

    @staticmethod
    async def get_user_data(user_id: str = "default_user") -> Dict[str, Any]:
        """Get user data including balance and subscribed funds"""
        try:
            response = user_funds_table.get_item(Key={"user_id": user_id})
            if "Item" not in response:
                # Create user if it doesn't exist
                user_data = {
                    "user_id": user_id,
                    "balance": INITIAL_BALANCE,
                    "subscribed_funds": []
                }
                user_funds_table.put_item(Item=user_data)
                return user_data
            return response['Item']
        except Exception as e:
            print(f"Error getting user data: {str(e)}")
            return {
                "user_id": user_id,
                "balance": INITIAL_BALANCE,
                "subscribed_funds": []
            }

    @staticmethod
    async def subscribe_to_fund(user_id: str, fund_id: str) -> Dict[str, Any]:
        """Subscribe user to a fund"""
        try:
            # Get fund details
            fund = await FundModel.get_fund(fund_id)
            if not fund:
                return {"success": False, "message": "Fund not found"}
            
            # Get user data
            user_data = await FundModel.get_user_data(user_id)
            
            # Check if user has enough balance
            if user_data["balance"] < fund["min_amount"]:
                return {
                    "success": False, 
                    "message": f"No tiene saldo disponible para vincularse al fondo {fund['name']}"
                }
            
            # Check if user is already subscribed to this fund
            subscribed_funds = user_data.get("subscribed_funds", [])
            if fund_id in [f["id"] for f in subscribed_funds]:
                return {"success": False, "message": f"Ya está vinculado al fondo {fund['name']}"}
            
            # Update user balance and add fund to subscribed funds
            new_balance = user_data["balance"] - fund["min_amount"]
            subscribed_funds.append({
                "id": fund_id,
                "name": fund["name"],
                "subscription_date": datetime.now().isoformat(),
                "amount": fund["min_amount"]
            })
            
            # Update user data in DynamoDB
            user_funds_table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET balance = :balance, subscribed_funds = :funds",
                ExpressionAttributeValues={
                    ":balance": new_balance,
                    ":funds": subscribed_funds
                }
            )
            
            # Create transaction record
            transaction_id = str(uuid.uuid4())
            transaction = {
                "id": transaction_id,
                "user_id": user_id,
                "fund_id": fund_id,
                "fund_name": fund["name"],
                "type": "SUBSCRIPTION",
                "amount": fund["min_amount"],
                "timestamp": datetime.now().isoformat()
            }
            transactions_table.put_item(Item=transaction)
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "message": f"Vinculación exitosa al fondo {fund['name']}",
                "new_balance": new_balance
            }
        except Exception as e:
            print(f"Error subscribing to fund: {str(e)}")
            return {"success": False, "message": "Error al procesar la solicitud"}

    @staticmethod
    async def unsubscribe_from_fund(user_id: str, fund_id: str) -> Dict[str, Any]:
        """Unsubscribe user from a fund"""
        try:
            # Get user data
            user_data = await FundModel.get_user_data(user_id)
            
            # Check if user is subscribed to the fund
            subscribed_funds = user_data.get("subscribed_funds", [])
            fund_subscription = None
            
            for fund in subscribed_funds:
                if fund["id"] == fund_id:
                    fund_subscription = fund
                    break
            
            if not fund_subscription:
                return {"success": False, "message": "No está vinculado a este fondo"}
            
            # Update user balance and remove fund from subscribed funds
            new_balance = user_data["balance"] + fund_subscription["amount"]
            updated_funds = [f for f in subscribed_funds if f["id"] != fund_id]
            
            # Update user data in DynamoDB
            user_funds_table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET balance = :balance, subscribed_funds = :funds",
                ExpressionAttributeValues={
                    ":balance": new_balance,
                    ":funds": updated_funds
                }
            )
            
            # Create transaction record
            transaction_id = str(uuid.uuid4())
            transaction = {
                "id": transaction_id,
                "user_id": user_id,
                "fund_id": fund_id,
                "fund_name": fund_subscription["name"],
                "type": "CANCELLATION",
                "amount": fund_subscription["amount"],
                "timestamp": datetime.now().isoformat()
            }
            transactions_table.put_item(Item=transaction)
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "message": f"Desvinculación exitosa del fondo {fund_subscription['name']}",
                "new_balance": new_balance
            }
        except Exception as e:
            print(f"Error unsubscribing from fund: {str(e)}")
            return {"success": False, "message": "Error al procesar la solicitud"} 