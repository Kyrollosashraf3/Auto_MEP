from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.EDA import DataAnalyzer , ReportGenerator

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


@router.get("/generate_report/{file_id}")
def generate_report(
    file_id: int,
    db: Session = Depends(get_db)
):
    data_analyzer = DataAnalyzer(db=db)
    calc = data_analyzer.basic_info(file_id=file_id)
    report_generator = ReportGenerator()
    result = report_generator.generate_summary(calc)
    return result
