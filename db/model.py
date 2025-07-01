from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import function
from db.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    task_id = Column(String, primary_key=True, index=True)
    file_name = Column(String)
    query = Column(Text)
    summary = Column(Text)
    content_excerpt = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
