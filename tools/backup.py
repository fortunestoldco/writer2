import asyncio
from datetime import datetime
import structlog
from typing import Optional
import aiofiles
import json

logger = structlog.get_logger(__name__)

class BackupManager:
    def __init__(self, mongodb_manager, backup_path: str = "backups/"):
        self.mongodb = mongodb_manager
        self.backup_path = backup_path

    async def create_backup(self, collection_name: str) -> Optional[str]:
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.backup_path}{collection_name}_{timestamp}.json"
            
            cursor = self.mongodb.db[collection_name].find({})
            documents = await cursor.to_list(length=None)
            
            async with aiofiles.open(filename, mode='w') as f:
                await f.write(json.dumps(documents, default=str))
            
            logger.info("backup_created", collection=collection_name, file=filename)
            return filename
        except Exception as e:
            logger.error("backup_failed", error=str(e))
            return None

    async def restore_backup(self, filename: str) -> bool:
        try:
            async with aiofiles.open(filename, mode='r') as f:
                content = await f.read()
                documents = json.loads(content)
            
            collection_name = filename.split('_')[0].split('/')[-1]
            await self.mongodb.db[collection_name].insert_many(documents)
            
            logger.info("backup_restored", collection=collection_name)
            return True
        except Exception as e:
            logger.error("restore_failed", error=str(e))
            return False