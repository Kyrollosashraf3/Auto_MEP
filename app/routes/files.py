from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.files import FileResponse

from app.services.file_service import FileService


router = APIRouter(
    prefix="/projects",
    tags=["Files"]
)


@router.post(
    "/{project_id}/files",
    response_model=FileResponse
)
def upload_file(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    return FileService.upload_file(
        db=db,
        project_id=project_id,
        file=file
    )