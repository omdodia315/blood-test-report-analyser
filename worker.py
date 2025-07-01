import dramatiq
import json
import redis
from tools import read_data_tool

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

    redis_client.setex(task_id, 3600, json.dumps(result))
    print("✅ Analysis complete and result saved.")
