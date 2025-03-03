# -*- coding: utf-8 -*-
import os
from typing import Any, Dict, List, Optional

import structlog
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings

logger = structlog.get_logger(__name__)


class MongoDBManager:
    """
    Manager for MongoDB operations.
    """

    def __init__(self):
        """Initialize the MongoDB manager."""
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]

    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection by name.

        Args:
            collection_name: Name of the collection to get.

        Returns:
            The requested collection.
        """
        return self.db[collection_name]

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def save_document(self, collection: str, document: Dict[str, Any]) -> str:
        """Save a document to MongoDB.

        Args:
            collection: Name of the collection to save the document in.
            document: The document to save.

        Returns:
            The ID of the saved document.
        """
        try:
            result = await self.db[collection].insert_one(document)
            logger.info(
                "document_saved",
                collection=collection,
                document_id=str(result.inserted_id),
            )
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(
                "mongodb_error",
                operation="save_document",
                error=str(e),
                collection=collection,
            )
            raise

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def find_document(
        self, collection: str, query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Find a document in MongoDB.

        Args:
            collection: Name of the collection to search in.
            query: Query to filter documents.

        Returns:
            The found document, or None if not found.
        """
        try:
            document = await self.db[collection].find_one(query)
            return document
        except PyMongoError as e:
            logger.error(
                "mongodb_error",
                operation="find_document",
                error=str(e),
                collection=collection,
                query=query,
            )
            raise
