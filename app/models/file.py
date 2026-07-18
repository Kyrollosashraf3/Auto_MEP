from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    file_name = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )