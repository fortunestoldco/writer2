from typing import Any, Dict, AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from agents.factory import AgentFactory
from config import MONGODB_CONFIG
from main import app
from mongodb import MongoDBManager, MongoManager
from workflows.manager import WorkflowManager
from .helpers import get_test_story_state


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
async def mongo_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    await client.close()


@pytest.fixture
def mongodb_manager():
    """Fixture for MongoDB manager."""
    return MongoDBManager()


@pytest.fixture
def agent_factory() -> AgentFactory:
    """Fixture for agent factory."""
    return AgentFactory()


@pytest.fixture
def workflow_manager(agent_factory: AgentFactory) -> WorkflowManager:
    return WorkflowManager(agent_factory)


@pytest.fixture
def test_input() -> Dict[str, Any]:
    """Fixture for test input data."""
    return {
        "title": "Test Story",
        "manuscript": "Test content",
        "model_provider": "anthropic",
        "model_name": "claude-3-opus-20240229",
    }


@pytest.fixture
def test_state() -> Dict[str, Any]:
    return get_test_story_state()
