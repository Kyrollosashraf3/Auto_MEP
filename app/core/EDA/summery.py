#app\core\EDA\summery.py

from app.core.EDA.prompt.prompt_builder import PromptBuilder
from app.core.llm.call_handler import call_model_family
from app.models.schemas import ChatRequest


class ReportGenerator:



    def generate_summary(self, calc: dict):

        prompt = PromptBuilder.build_project_summary(calc)

        req = ChatRequest(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        resp = call_model_family(req)
        return resp
