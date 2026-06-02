from openai import AsyncOpenAI
import os
import json
from config import OPENROUTER_API_KEY, LLM_MODEL

class Planner:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            timeout=30.0
        )
        self.model = LLM_MODEL
    
    async def think(self, prompt: str) -> str:
    try:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        result = response.choices[0].message.content
        if not result or result.strip() == "":
            return "Извините, не удалось сформировать ответ."
        return result
    except Exception as e:
        print(f"OpenRouter error: {e}")
        return f"Ошибка API: {str(e)}"
