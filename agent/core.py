from agent.planner import Planner
from agent.memory import Memory

class Agent:
    def __init__(self, memory: Memory):
        self.planner = Planner()
        self.memory = memory
    
    async def process(self, user_id: int, message: str) -> str:
        self.memory.add_message(user_id, "user", message)
        history = self.memory.get_history(user_id)
        prompt = f"""Ответь на сообщение.
История: {history[-5:]}
Сообщение: {message}
Ответь кратко:"""
        response = await self.planner.think(prompt)
        self.memory.add_message(user_id, "assistant", response)
        return response
