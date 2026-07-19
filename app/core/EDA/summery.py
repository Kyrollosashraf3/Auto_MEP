#app\core\EDA\summery.py

from app.core.EDA.prompt.prompt_builder import PromptBuilder
from app.core.llm.call_handler import call_model_family
from app.models.schemas import ChatRequest
from app.config.settings import settings

class ReportGenerator:

#gemini-2.5-flash
#llama-3.1-8b-instant
#gemini-2.0-flash-lite
    def generate_summary(self, calc: dict):

        prompt = PromptBuilder.build_project_summary(calc)

        req = ChatRequest(
            model= settings.cooling_report_model,
            messages=[{"role": "user", "content": prompt}]
        )

        resp = call_model_family(req)

        return resp
