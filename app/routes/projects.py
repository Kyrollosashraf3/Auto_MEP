from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from typing import List
from app.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectDetailsResponse,
    ProjectUpdate
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


@router.delete(
    "/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ProjectService.delete_project(
            db=db,
            project_id=project_id,
            user_id=current_user.id
        )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return ProjectService.update_project(
            db=db,
            project_id=project_id,
            user_id=current_user.id,
            project_data=project_data
        )
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))





@router.get(
    "/id/{project_id}",
    response_model=ProjectDetailsResponse
)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ProjectService.get_project_by_id(
        db=db,
        project_id=project_id,
        owner_id=current_user.id
    )


@router.get(
    "/name/{project_name}",
    response_model=ProjectDetailsResponse
)
def get_project_by_name(
    project_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ProjectService.get_project_by_name(
        db=db,
        project_name=project_name,
        owner_id=current_user.id
    )
