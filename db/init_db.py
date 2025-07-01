import asyncio
from db.database import engine, Base
from db.models import AnalysisResult

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database and tables created successfully.")

asyncio.run(init())
