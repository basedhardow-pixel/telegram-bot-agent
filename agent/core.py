from agent.planner import Planner
from agent.memory import Memory
from agent.tools import Tools

class Agent:
    def __init__(self, memory: Memory):
        self.planner = Planner()
        self.memory = memory
        self.tools = Tools()
    
    async def process(self, user_id: int, message: str) -> str:
        self.memory.add_message(user_id, "user", message)
        
        message_lower = message.lower()
        
        if "найди" in message_lower or "поищи" in message_lower or "google" in message_lower:
            query = message.replace("найди", "").replace("поищи", "").strip()
            return await self.tools.search_web(query)
        
        if "погода" in message_lower:
            city = message_lower.replace("погода", "").replace("в", "").strip()
            if not city:
                city = "Москва"
            return await self.tools.get_weather(city)
        
        if "курс" in message_lower or "доллар" in message_lower or "евро" in message_lower:
            currency = "USD"
            if "евро" in message_lower:
                currency = "EUR"
            return await self.tools.get_exchange_rate(currency)
        
        if any(op in message_lower for op in ["+", "-", "*", "/"]):
            return await self.tools.calculate(message)
        
        if "время" in message_lower or "час" in message_lower:
            return await self.tools.get_time()
        
        history = self.memory.get_history(user_id)
        prompt = f"""Ответь на сообщение пользователя.
История: {history[-3:]}
Сообщение: {message}
Ответь кратко и полезно:"""
        
        response = await self.planner.think(prompt)
        
        if not response or response.strip() == "":
            response = "Не удалось получить ответ."
        
        self.memory.add_message(user_id, "assistant", response)
        return response