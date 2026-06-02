import redis
import json
from typing import List, Dict

class Memory:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    def add_message(self, user_id: int, role: str, content: str):
        key = f"history:{user_id}"
        message = {"role": role, "content": content}
        history = self.get_history(user_id)
        history.append(message)
        # БЕЗ ЛИМИТА - сохраняем всё
        self.redis.set(key, json.dumps(history))
    
    def get_history(self, user_id: int) -> List[Dict]:
        key = f"history:{user_id}"
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return []
    
    def clear_history(self, user_id: int):
        key = f"history:{user_id}"
        self.redis.delete(key)
    
    def save_fact(self, user_id: int, fact: str):
        key = f"facts:{user_id}"
        facts = self.get_facts(user_id)
        facts.append(fact)
        # Факты тоже без лимита
        self.redis.set(key, json.dumps(facts))
    
    def get_facts(self, user_id: int) -> List[str]:
        key = f"facts:{user_id}"
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return []