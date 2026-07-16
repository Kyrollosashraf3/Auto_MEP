from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.project import ProjectCreate

from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db)
):

    return ProjectService.create_project(
        db=db,
        name=payload.name,
        description=payload.description,
        owner_id=1
    )


@router.get("/")
def get_projects(
    db: Session = Depends(get_db)
):

    return db.query(Project).all()