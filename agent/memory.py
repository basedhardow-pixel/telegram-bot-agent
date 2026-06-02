import redis
import json
from typing import List, Dict

class Memory:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True, protocol=2)
        self.history_limit = 20
    
    def add_message(self, user_id: int, role: str, content: str):
        key = f"history:{user_id}"
        message = {"role": role, "content": content}
        history = self.get_history(user_id)
        history.append(message)
        if len(history) > self.history_limit:
            history = history[-self.history_limit:]
        self.redis.set(key, json.dumps(history))
    
    def get_history(self, user_id: int) -> List[Dict]:
        key = f"history:{user_id}"
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return []
