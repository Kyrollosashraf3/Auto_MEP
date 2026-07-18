from pydantic import BaseModel
from datetime import datetime


class FileResponse(BaseModel):

    id: int
    project_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
        