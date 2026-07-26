from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.EDA import DataAnalyzer , ReportGenerator
from app.core.file.pdf_generator import PDFGenerator

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/{file_id}")
def analyze_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    analyzer = DataAnalyzer(db)

    analysis_result = analyzer.basic_info(file_id)
    calc = analysis_result["calc"]

    return calc


@router.get("/{file_id}/download")
def download_analysis(
    file_id: int,
    db: Session = Depends(get_db)
):
    analyzer = DataAnalyzer(db)

    analysis_result = analyzer.basic_info(file_id)

    calc = analysis_result["calc"]
    file_name = analysis_result["file_name"]
    project_name = analysis_result["project_name"]


    pdf_path = PDFGenerator.generate(
        file_name=file_name,
        project_name=project_name,
        content=calc,
    )

    safe_file = file_name.rsplit(".", 1)[0].replace(" ", "_").replace("/", "_")
    safe_project = project_name.replace(" ", "_").replace("/", "_")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{safe_file}_{safe_project}_analysis.pdf"
    )


#--------------------------------------


@router.get("/generate_report/{file_id}")
def generate_report(
    file_id: int,
    db: Session = Depends(get_db)
):
    analyzer = DataAnalyzer(db)

    analysis_result = analyzer.basic_info(file_id)
    
    calc = analysis_result["calc"]

    report = ReportGenerator().generate_summary(calc)

    return report



@router.get("/generate_report/{file_id}/download")
def download_report(
    file_id: int,
    db: Session = Depends(get_db)
):
    analyzer = DataAnalyzer(db)
    analysis_result = analyzer.basic_info(file_id)
    
    calc = analysis_result["calc"]
    file_name = analysis_result["file_name"]
    project_name = analysis_result["project_name"]


    report = ReportGenerator().generate_summary(calc)

    pdf_path = PDFGenerator.generate(
        file_name= file_name,
        project_name= project_name,
        content=report["text"],
    )

    safe_file = file_name.rsplit(".", 1)[0].replace(" ", "_").replace("/", "_")
    safe_project = project_name.replace(" ", "_").replace("/", "_")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{safe_file}_{safe_project}_report.pdf"
    )

