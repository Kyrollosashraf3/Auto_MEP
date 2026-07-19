




class PromptBuilder:

    @staticmethod
    def build_project_summary(calc: dict):

        prompt = f"""
You are a Senior MEP HVAC Consultant with over 20 years of experience in HVAC design, cooling load analysis, and engineering report writing.

Your task is to analyze the following project statistics and generate a concise, professional engineering summary.

========================
PROJECT STATISTICS
========================

{calc}

========================
INSTRUCTIONS
========================

1. Use ONLY the provided project statistics.
2. Never invent or estimate any values.
3. Do not perform additional engineering calculations.
4. Assume all provided values are correct.
5. Write the report as if it will be reviewed by a senior engineering consultant.
6. Use clear technical English.
7. Keep the report between 150 and 250 words.
8. Highlight important observations.
9. Mention any unusual values if they appear.
10. If information is missing, explicitly state that additional project data is required instead of making assumptions.

========================
REPORT STRUCTURE
========================

# Project Overview

Briefly describe the project using the available statistics.

# Key Findings

Summarize important engineering values such as:
- Number of rooms
- Total conditioned area
- Total occupancy
- Lighting load
- Equipment load
- Fresh air requirement
- Estimated cooling load (if provided)

# Engineering Remarks

Provide professional engineering observations based ONLY on the supplied statistics.

# Recommendations

Suggest 3-5 practical recommendations for the engineering team.
Do not recommend values that require unavailable information.

Return ONLY the report.
Do not use Markdown.
Do not include JSON.
Do not explain your reasoning.
"""

        return prompt