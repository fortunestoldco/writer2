from typing import AsyncGenerator, Dict
from fastapi import Depends
from mongodb import MongoDBManager
from agents import AgentFactory
from prometheus_client import Counter
from contextlib import asynccontextmanager

# Tracking metrics
db_operations = Counter(
    'database_operations_total',
    'Number of database operations',
    ['operation_type']
)

@asynccontextmanager
async def get_mongodb() -> AsyncGenerator[MongoDBManager, None]:
    """Get MongoDB connection with metrics tracking"""
    mongodb = MongoDBManager()
    try:
        yield mongodb
    finally:
        await mongodb.close()

async def get_agent_factory(
    mongodb: MongoDBManager = Depends(get_mongodb)
) -> AgentFactory:
    """Get agent factory with dependency injection"""
    return AgentFactory(mongodb)