from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from typing import List
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse
)

from app.services.project_service import ProjectService
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return ProjectService.create_project(
            db=db,
            project_data=project_data,
            owner_id=current_user.id
    )


@router.get(
    "",
    response_model=List[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return ProjectService.get_projects( 
            db=db,
            owner_id=current_user.id)
