import google.generativeai as genai

from config import settings
from research.prompts import RESEARCH_MENTOR_PROMPT


genai.configure(api_key=settings.GEMINI_API_KEY)


class ResearchAnalyzer:

    def __init__(self):
        self.model = genai.GenerativeModel(
            settings.MODEL_NAME
        )

    def analyze_project(
        self,
        project_text: str,
        max_words: int = 700
    ) -> str:

        prompt = f"""
{RESEARCH_MENTOR_PROMPT}

Keep the full review under {max_words} words.

Uploaded Project Content:
{project_text}

Richard Feynman's Review:
"""

        response = self.model.generate_content(prompt)

        return response.text