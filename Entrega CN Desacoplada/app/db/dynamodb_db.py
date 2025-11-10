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
                table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'athlete_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'athlete_id',
                            'AttributeType': 'S'
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                
                table.wait_until_exists()
                
                self.table = table
            else:
                raise
    
    def create_athlete(self, athlete: Athlete) -> Athlete:
        self.table.put_item(Item=athlete.model_dump())
        return athlete
    
    def get_athlete(self, athlete_id: str) -> Optional[Athlete]:
        response = self.table.get_item(Key={'athlete_id': athlete_id})
        if 'Item' in response:
            return Athlete(**response['Item'])
        return None
    
    def get_all_athletes(self) -> List[Athlete]:
        response = self.table.scan()
        athletes = [Athlete(**item) for item in response.get('Items', [])]
        return sorted(athletes, key=lambda x: x.Number)
    
    def update_athlete(self, athlete_id: str, athlete: Athlete) -> Optional[Athlete]:
        athlete.update_timestamp()
        athlete.athlete_id = athlete_id
        self.table.put_item(Item=athlete.model_dump())
        return athlete
    
    def delete_athlete(self, athlete_id: str) -> bool:
        response = self.table.delete_item(
            Key={'athlete_id': athlete_id},
            ReturnValues='ALL_OLD'
        )
        return 'Attributes' in response