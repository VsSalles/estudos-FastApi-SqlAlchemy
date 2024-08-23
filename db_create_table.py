from core.database import engine
from core.config import settings
import asyncio
from models.faculdade import *

async def create_tables():
    async with engine.begin() as coon:
        await coon.run_sync(settings.DB_BASE.metadata.drop_all)
        await coon.run_sync(settings.DB_BASE.metadata.create_all)
        

if __name__ == '__main__':
    asyncio.run(create_tables())