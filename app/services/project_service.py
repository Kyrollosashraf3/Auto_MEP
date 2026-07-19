from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.file import File

from app.schemas.project import ProjectCreate, ProjectDetailsResponse, ProjectUpdate
from fastapi import HTTPException


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

    @staticmethod
    def delete_project(
        db: Session,
        project_id: int,
        user_id: int
    ):
        project = (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == user_id
            )
            .first()
        )

        if not project:
            raise ValueError("Project not found")
        
        if project.owner_id != user_id:
            return {"message": f"You are not authorized to delete this project .... this project id: ( {project.id} ) is releted to USER id:( {project.owner_id} )"}

        db.delete(project)
        db.commit()

        return {
            "message": f"Project {project_id} deleted successfully"
        }

    @staticmethod
    def update_project(
        db: Session,
        project_id: int,
        user_id: int,
        project_data: ProjectUpdate
    ):
        project = (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == user_id
            )
            .first()
        )

        if not project:
            raise ValueError("Project not found")

        project.name = project_data.name
        project.description = project_data.description

        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_project_by_id(
        db: Session,
        project_id: int,
        owner_id: int
    ):

       
        project = (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == owner_id
            )
            .first()
        )

        if not project:
            raise HTTPException(status_code=404, detail=f"Project with id ({project_id}) not found or access denied")

        files = (
            db.query(File)
            .filter(File.project_id == project.id)
            .all()
        )

        return ProjectDetailsResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            files=files,
            created_at=project.created_at
        )

    @staticmethod
    def get_project_by_name(
        db: Session,
        project_name: str,
        owner_id: int
    ):
        project = (
            db.query(Project)
            .filter(
                Project.name.ilike(f"%{project_name}%"),
                Project.owner_id == owner_id
            )
            .first()
        )

        if not project:
            raise HTTPException(status_code=404, detail=f"Project with name '{project_name}' not found or access denied")

        files = (
            db.query(File)
            .filter(File.project_id == project.id)
            .all()
        )

        return ProjectDetailsResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            files=files,
            created_at=project.created_at
        )