import pytest
from fastapi.testclient import TestClient
from moto import mock_dynamodb
import boto3
import os
import json

from app.main import app
from app.api.models.fund import FundModel

client = TestClient(app)

# Set up mock DynamoDB
@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for boto3"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb():
        # Create DynamoDB tables
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create Funds table
        dynamodb.create_table(
            TableName='Funds',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}  # Primary key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Create UserFunds table
        dynamodb.create_table(
            TableName='UserFunds',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}  # Primary key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Create Transactions table
        dynamodb.create_table(
            TableName='Transactions',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'id-index',
                    'KeySchema': [
                        {'AttributeName': 'id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Initialize database
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(FundModel.initialize_database())
        
        yield dynamodb

# Test getting all funds
def test_get_all_funds(dynamodb):
    response = client.get("/api/funds/")
    assert response.status_code == 200
    funds = response.json()
    assert len(funds) == 5
    assert funds[0]["name"] == "FPV_EL CLIENTE_RECAUDADORA"

# Test getting user funds
def test_get_user_funds(dynamodb):
    response = client.get("/api/funds/user")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["balance"] == 500000
    assert len(user_data["subscribed_funds"]) == 0

# Test subscribing to a fund
def test_subscribe_to_fund(dynamodb):
    # First, try to subscribe to a fund
    response = client.post(
        "/api/funds/subscribe",
        json={"fund_id": "1"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert result["new_balance"] == 425000  # 500000 - 75000
    
    # Check user data after subscription
    response = client.get("/api/funds/user")
    user_data = response.json()
    assert user_data["balance"] == 425000
    assert len(user_data["subscribed_funds"]) == 1
    assert user_data["subscribed_funds"][0]["id"] == "1"
    
    # Check transactions
    response = client.get("/api/transactions/")
    transactions = response.json()
    assert len(transactions) == 1
    assert transactions[0]["type"] == "SUBSCRIPTION"
    assert transactions[0]["fund_id"] == "1"

# Test insufficient balance
def test_insufficient_balance(dynamodb):
    # First, subscribe to funds to reduce balance
    client.post("/api/funds/subscribe", json={"fund_id": "1"})  # -75000
    client.post("/api/funds/subscribe", json={"fund_id": "2"})  # -125000
    client.post("/api/funds/subscribe", json={"fund_id": "3"})  # -50000
    
    # Try to subscribe to an expensive fund
    response = client.post(
        "/api/funds/subscribe",
        json={"fund_id": "4"}  # 250000
    )
    assert response.status_code == 400
    assert "No tiene saldo disponible" in response.json()["detail"]

# Test unsubscribing from a fund
def test_unsubscribe_from_fund(dynamodb):
    # First, subscribe to a fund
    client.post("/api/funds/subscribe", json={"fund_id": "1"})
    
    # Then unsubscribe
    response = client.post(
        "/api/funds/unsubscribe",
        json={"fund_id": "1"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert result["new_balance"] == 500000  # Back to original
    
    # Check user data after unsubscription
    response = client.get("/api/funds/user")
    user_data = response.json()
    assert user_data["balance"] == 500000
    assert len(user_data["subscribed_funds"]) == 0
    
    # Check transactions
    response = client.get("/api/transactions/")
    transactions = response.json()
    assert len(transactions) == 2  # Subscription + Cancellation
    assert transactions[0]["type"] == "CANCELLATION"
    assert transactions[0]["fund_id"] == "1" 