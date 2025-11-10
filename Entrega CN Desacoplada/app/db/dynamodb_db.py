import boto3
from botocore.exceptions import ClientError
from typing import List, Optional
from app.db.db import Database
from app.model.athlete import Athlete
import os

class DynamoDBDatabase(Database):
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        # Prefer TABLE_NAME as set in the CloudFormation template, but allow legacy DB_DYNAMONAME
        self.table_name = os.getenv('TABLE_NAME') or os.getenv('DB_DYNAMONAME')
        self.table = self.dynamodb.Table(self.table_name)
        self.initialize()
    
    def initialize(self):
        try:
            self.table.load()
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                # La tabla no existe, crearla
                print(f"Creando tabla DynamoDB '{self.table_name}'...")
                # Create table using Number as primary key (numeric)
                table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'Number',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'Number',
                            'AttributeType': 'N'
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                
                table.wait_until_exists()
                
                self.table = table
            else:
                raise
    
    def create_athlete(self, athlete: Athlete) -> Athlete:
        # Expect athlete.Number to be set and unique
        self.table.put_item(Item=athlete.model_dump())
        return athlete
    
    def get_athlete(self, athlete_number: int) -> Optional[Athlete]:
        response = self.table.get_item(Key={'Number': athlete_number})
        if 'Item' in response:
            return Athlete(**response['Item'])
        return None
    
    def get_all_athletes(self) -> List[Athlete]:
        response = self.table.scan()
        athletes = [Athlete(**item) for item in response.get('Items', [])]
        return sorted(athletes, key=lambda x: x.Number)
    
    def update_athlete(self, athlete_number: int, athlete: Athlete) -> Optional[Athlete]:
        athlete.update_timestamp()
        athlete.Number = athlete_number
        self.table.put_item(Item=athlete.model_dump())
        return athlete
    
    def delete_athlete(self, athlete_number: int) -> bool:
        response = self.table.delete_item(
            Key={'Number': athlete_number},
            ReturnValues='ALL_OLD'
        )
        return 'Attributes' in response