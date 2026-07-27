from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.files import FileResponse

from app.services.file_service import FileService
from app.config.logger import get_logger

logger = get_logger(__name__)

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
    logger.info(f"Uploading file '{file.filename}' to project {project_id}")
    return FileService.upload_file(
        db=db,
        project_id=project_id,
        file=file
    )



@router.delete(
    "/{project_id}/files"
)
def delete_file(
    project_id: int,
    file_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting file {file_id} from project {project_id}")
    try:
        return FileService.delete_file(
            db=db,
            project_id=project_id,
            file_id=file_id
        )
    except ValueError as e:
        logger.warning(f"File delete failed: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))