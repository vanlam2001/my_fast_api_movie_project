from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

DATABASE_URL = "mongodb+srv://vanlam1412:5DFv9zNIh4bQaYBY@cluster0.8eouv1s.mongodb.net"

async def get_database() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(DATABASE_URL)
    database = client.get_database("register")
    yield database
    client.close()


    