import os
from databases.db import Database
from databases.dynamodb_db import DynamoDBDatabase


class DatabaseFactory:

    @classmethod
    def create(cls) -> Database:
        return DynamoDBDatabase()

    @classmethod
    def get_available_databases(cls) -> list:
        return ["dynamodb"]
