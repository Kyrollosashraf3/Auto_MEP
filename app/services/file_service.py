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


    @staticmethod
    def delete_file(
        db: Session,
        project_id: int,
        file_id: int
    ):
        file_record = (
            db.query(File)
            .filter(
                File.id == file_id,
                File.project_id == project_id
            )
            .first()
        )

        if not file_record:
            raise ValueError("File not found")

        import os
        if file_record.file_path and os.path.exists(file_record.file_path):
            try:
                os.remove(file_record.file_path)
            except Exception:
                pass

        db.delete(file_record)
        db.commit()

        return {"message": "File deleted successfully"}