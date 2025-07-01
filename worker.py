import dramatiq
import json
import redis
from tools import read_data_tool
from db.database import SessionLocal
from db.models import AnalysisResult
import asyncio

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@dramatiq.actor
def analyze_pdf_task(file_path, query, task_id):
    print(f"📄 Starting analysis for: {file_path} | Query: {query}")

    content = read_data_tool(file_path)
    result = {
        "status": "completed",
        "summary": f"Processed file: {file_path}",
        "query": query,
        "content_excerpt": content[:500]
    }

    # ✅ Save to Redis (temporary)
    redis_client.setex(task_id, 3600, json.dumps(result))
    print("✅ Result saved to Redis.")

    # ✅ Save to SQLite (permanent)
    async def save_to_db():
        async with SessionLocal() as session:
            entry = AnalysisResult(
                task_id=task_id,
                file_name=file_path,
                query=query,
                summary=result["summary"],
                content_excerpt=result["content_excerpt"]
            )
            session.add(entry)
            await session.commit()
            print("✅ Result also saved to SQLite database.")

    asyncio.run(save_to_db())
