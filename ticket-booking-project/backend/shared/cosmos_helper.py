import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

ENDPOINT = os.environ["COSMOS_ENDPOINT"]
KEY = os.environ["COSMOS_KEY"]
DB_NAME = os.environ.get("COSMOS_DB_NAME", "ticketing-db")

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = CosmosClient(ENDPOINT, credential=KEY)
        _db = _client.get_database_client(DB_NAME)
    return _db

def get_container(name: str):
    return get_db().get_container_client(name)
