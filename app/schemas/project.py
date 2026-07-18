from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas import FileResponse

class ProjectCreate(BaseModel):

    name: str
    description: str | None = None
    

class ProjectResponse(BaseModel):

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True



class ProjectDetailsResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    files: List[FileResponse]
   

    class Config:
        from_attributes = True