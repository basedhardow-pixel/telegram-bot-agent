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
        models_to_try = [
            self.model,
            "openrouter/free",
            "microsoft/phi-3-mini-128k-instruct:free"
        ]
        
        for model in models_to_try:
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.7,
                    timeout=15.0
                )
                result = response.choices[0].message.content
                if result and result.strip():
                    return result
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
        
        return "Извините, сейчас не могу ответить. Попробуйте позже."
    
    async def parse_intent(self, message: str) -> dict:
        prompt = f"""Определи намерение. Ответь ТОЛЬКО JSON.
Сообщение: {message}
Варианты: question, action, memory
Пример ответа: {{"intent": "question", "entity": null}}"""
        
        try:
            response = await self.think(prompt)
            return json.loads(response)
        except:
            return {"intent": "question", "entity": None}