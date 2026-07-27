#app\core\EDA\summery.py

from app.core.EDA.prompt.prompt_builder import PromptBuilder
from app.core.llm.call_handler import call_model_family
from app.models.schemas import ChatRequest
from app.models.analysis_result import AnalysisResult
from app.config.settings import settings

class ReportGenerator:

    def __init__(self, db=None):
        self.db = db

    def get_cached_report(self, file_id: int):
        if not self.db:
            return None
        return (
            self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.file_id == file_id,
                AnalysisResult.type == "report"
            )
            .first()
        )

    def save_report(self, file_id: int, report, file_name: str, project_name: str):
        if not self.db:
            return
        existing = self.get_cached_report(file_id)
        if existing:
            existing.result_json = report
            existing.file_name = file_name
            existing.project_name = project_name
        else:
            existing = AnalysisResult(
                file_id=file_id,
                type="report",
                result_json=report,
                file_name=file_name,
                project_name=project_name,
            )
            self.db.add(existing)
        self.db.commit()
        self.db.refresh(existing)

    def generate_summary(self, calc: dict, file_id: int = None, file_name: str = "", project_name: str = ""):

        if file_id and self.db:
            cached = self.get_cached_report(file_id)
            if cached:
                return cached.result_json

        prompt = PromptBuilder.build_project_summary(calc)

        req = ChatRequest(
            model= settings.cooling_report_model,
            messages=[{"role": "user", "content": prompt}]
        )

        resp = call_model_family(req)
        

        if file_id and self.db:
            self.save_report(file_id, resp, file_name, project_name)

        return resp
