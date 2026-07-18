from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.EDA.analyzer import DataAnalyzer

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/{file_id}")
def analyze_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    data_analyzer = DataAnalyzer(db=db)
    result = data_analyzer.basic_info(file_id=file_id)
    return result