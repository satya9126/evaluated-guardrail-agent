from openai import OpenAI

from app.core.config import settings


class LLMService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def generate(self, message: str) -> str:

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content