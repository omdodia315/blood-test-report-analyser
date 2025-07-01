import os
import uuid
import redis
import json
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from worker import analyze_pdf_task
from db.database import SessionLocal
from db.models import AnalysisResult

app = FastAPI(title="Blood Test Report Analyser")

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    task_id = str(uuid.uuid4())

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        analyze_pdf_task.send(file_path, query, task_id)
        redis_client.setex(task_id, 3600, "PENDING")

        return {
            "status": "submitted",
            "task_id": task_id,
            "file_processed": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    # Try Redis first
    result = redis_client.get(task_id)
    if result and result != "PENDING":
        try:
            return json.loads(result)
        except Exception:
            return {"status": result}

    # Fallback to DB (if Redis expired or skipped)
    async with SessionLocal() as session:
        record = await session.get(AnalysisResult, task_id)
        if record:
            return {
                "status": "completed",
                "task_id": record.task_id,
                "summary": record.summary,
                "query": record.query,
                "file_name": record.file_name,
                "content_excerpt": record.content_excerpt
            }

    return {"status": "not_found_or_expired"}
