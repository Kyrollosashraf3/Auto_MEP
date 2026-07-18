from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate
from app.core.deps import get_current_user
from app.db.database import get_db
from fastapi import Depends


class ProjectService:

    @staticmethod
    def create_project(
        db: Session,
        project_data: ProjectCreate,
        owner_id: int
    ):

        project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=owner_id
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project

    @staticmethod
    def get_projects(
        db: Session,
        owner_id: int
    ):
        return (
            db.query(Project)
            .filter(
                Project.owner_id == owner_id
            )
            .all()
        )