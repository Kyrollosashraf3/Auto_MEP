from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, UniqueConstraint
from datetime import datetime
from app.db.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    type = Column(String, nullable=False)  # "analysis" or "report"
    result_json = Column(JSON, nullable=False)
    file_name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("file_id", "type", name="uq_file_type"),
    )