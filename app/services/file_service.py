import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.file import File
from app.core.file.data_control import DataControl


class FileService:

    @staticmethod
    def upload_file(
        db: Session,
        project_id: int,
        file: UploadFile
    ):

        dc = DataControl()

        is_valid = dc.validate_uploaded_file(file)

        if not is_valid:
            raise ValueError("Invalid file")

        file_path, file_id = dc.generate_unique_filepath(
            orig_file_name=file.filename,
            project_id=str(project_id)
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        file_record = File(
            project_id=project_id,
            file_name=file.filename,
            file_path=file_path
        )

        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        return file_record