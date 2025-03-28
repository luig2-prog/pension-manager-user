import uvicorn
import os
import boto3
import json
from moto import mock_dynamodb, mock_ses, mock_sns

from app.api.models.fund import FundModel

# Use moto to mock AWS services for local development
dynamodb_mock = mock_dynamodb()
ses_mock = mock_ses()
sns_mock = mock_sns()

# Start mocks
dynamodb_mock.start()
ses_mock.start()
sns_mock.start()

# Set DynamoDB endpoint to localhost:8001 to match docker-compose configuration
os.environ['DYNAMODB_ENDPOINT'] = 'http://localhost:8001'

# Create DynamoDB tables
dynamodb = boto3.resource(
    'dynamodb', 
    region_name='us-east-1',
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', None)
)

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

# Initialize the database with sample data
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(FundModel.initialize_database())

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# Clean up mocks on exit
import atexit

def cleanup():
    dynamodb_mock.stop()
    ses_mock.stop()
    sns_mock.stop()

atexit.register(cleanup) 