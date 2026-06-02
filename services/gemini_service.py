import google.generativeai as genai

from config import settings
from persona.feynman_persona import FEYNMAN_PERSONA


genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:

    def __init__(self):
        self.model = genai.GenerativeModel(
            settings.MODEL_NAME
        )

    def generate_response(
        self,
        question: str,
        context: str,
        memories: list[str] | None = None,
        max_words: int = 125
    ):

        memory_text = "No relevant user memories found."

        if memories:
            memory_text = "\n".join(
                f"- {memory}" for memory in memories
            )

        prompt = f"""
{FEYNMAN_PERSONA}

You must answer using the provided context.
If the answer is not clearly supported by the context, say so honestly.
Keep the answer under 125 words.

Relevant User Memories:
{memory_text}

Retrieved Feynman Knowledge:
{context}

User Question:
{question}

Answer as Richard Feynman:
"""

        response = self.model.generate_content(
            prompt
        )

        return response.text