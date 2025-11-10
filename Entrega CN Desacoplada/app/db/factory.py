import os
from app.db.db import Database
from app.db.dynamodb_db import DynamoDBDatabase


class DatabaseFactory:

    @classmethod
    def create(cls) -> Database:
        return DynamoDBDatabase()

    @classmethod
    def get_available_databases(cls) -> list:
        return ["dynamodb"]
